from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import datetime
import openai
import base64
import re

app = FastAPI()

# ✅ Разрешаем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ⚠️ Твой OpenAI ключ
openai.api_key = "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"


@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    print(f"📥 Получен файл: {file.filename}")

    # Чтение файла и base64 кодирование
    image_bytes = await file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")

    # Отправка изображения в GPT-4-Vision
    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_base64}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Что на фото? Сколько примерно калорий в этом блюде? Дай краткое описание и обязательно точное количество калорий числом."
                    }
                ]
            }
        ],
        max_tokens=300,
    )

    result_text = response.choices[0].message.content
    print("📤 Ответ от GPT:", result_text)

    # 🔍 Извлекаем калории числом (первое число перед "ккал" или "kcal")
    calorie_match = re.search(r"(\d{2,4})\s?(?:ккал|kcal)", result_text.lower())
    calories = int(calorie_match.group(1)) if calorie_match else 0

    return {
        "name": "Meal",  # Позже можно тоже извлекать из текста
        "calories": calories,
        "description": result_text,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
