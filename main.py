from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import datetime

# 🧠 Функции из твоего модуля
from openai_api import query_openai_image, parse_response_to_structured_format

app = FastAPI()

# ✅ Настройка CORS — чтобы FlutterFlow не блокировал запросы
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить до домена
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    print(f"📥 Получен файл: {file.filename}")

    # 📸 Считываем изображение
    image_bytes = await file.read()

    # 🎯 Отправляем в OpenAI и получаем сырой ответ
    response_text = query_openai_image(image_bytes)

    # 🧹 Парсим его в твою структуру: name, calories, description
    structured = parse_response_to_structured_format(response_text)

    # 🕒 Добавляем время
    structured["timestamp"] = datetime.datetime.utcnow().isoformat()

    return structured
