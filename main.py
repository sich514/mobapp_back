from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import datetime

app = FastAPI()

# ✅ Разрешаем CORS, чтобы запросы с FlutterFlow не блокировались
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить до конкретного домена
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    print(f"📥 Получен файл: {file.filename}")
    
    # В будущем сюда добавится логика обработки изображения

    return {
        "name": "Pineapple",
        "calories": "100 kcal",
        "description": "A meal is a serving of food, or an occasion when food is eaten, often at regular times like breakfast, lunch, or dinner. Meals can be simple or elaborate, and they can be planned or spontaneous."
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
