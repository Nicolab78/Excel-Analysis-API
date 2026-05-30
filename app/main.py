from fastapi import FastAPI
from fastapi import UploadFile
import shutil
from pathlib import Path
import uuid
import pandas as pd



app = FastAPI()

@app.get("/")
def root():
    """Endpoint racine de l'API"""
    return {"message":"Excel Analysis API"}

@app.get("/health")
def health_check():
    """Vérifie si l'API fonctionne"""
    return {"status":"OK"}

@app.post("/upload")
async def upload_file(file: UploadFile):
    """Upload un fichier CSV ou Excel"""

    file_id = str(uuid.uuid4())

    file_extension = Path(file.filename).suffix
    file_path = Path("uploads") / f"{file_id}{file_extension}"

    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_id" : file_id,
        "filename" : file.filename,
        "message" : "Fichier uploadé avec succès"
    }


@app.get("/analyse/{file_id}")
async def analyse(file_id: str):
    """Analyse un fichier CSV ou Excel"""
    
    fichiers = list(Path("uploads").glob(f"{file_id}*"))
    
    if not fichiers:
        return {"error": "Fichier non trouvé"}
    
    file_path = fichiers[0]
    
    if file_path.suffix == ".xlsx":
        df = pd.read_excel(file_path)
    else:
        df = pd.read_csv(file_path)
    
    analyse = {
        "nb_lignes": len(df),
        "nb_colonnes": len(df.columns),
        "colonnes": df.columns.tolist(),
        "types_donnees": df.dtypes.astype(str).to_dict(),
        "stats": df.describe().to_dict(),
        "valeurs_manquantes": df.isnull().sum().to_dict()
    }
    
    return {
        "file_id": file_id,
        "filename": file_path.name,
        "analyse": analyse
    }
