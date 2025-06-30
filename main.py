from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from typing import Dict
import datetime

app = FastAPI()

@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile):
    # Здесь позже будет AI логика (в будущем)
    
    return {
        "name": "Яблоко",
        "calories": 100,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
