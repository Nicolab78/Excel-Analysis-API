from fastapi import FastAPI
from fastapi import UploadFile
import shutil
from pathlib import Path
import uuid

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