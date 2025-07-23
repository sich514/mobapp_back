from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import datetime
import base64

from openai import OpenAI

# 🔐 Твой API-ключ
client = OpenAI(api_key='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')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def encode_image_bytes(image_bytes: bytes) -> str:
    return f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"

@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    print(f"📥 Получен файл: {file.filename}")

    # ⬇️ Чтение изображения из запроса
    image_bytes = await file.read()
    base64_image = encode_image_bytes(image_bytes)

    # 📡 Запрос к OpenAI Vision (gpt-4.1)
    response = client.responses.create(
        model="gpt-4.1",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Если на изображении есть еда — посчитай её суммарную калорийность. "
                            "Верни только одно число, например: 520"
                        )
                    },
                    {
                        "type": "input_image",
                        "image_url": base64_image,
                    }
                ]
            }
        ]
    )

    raw = response.output_text.strip()
    print(f"🔎 Ответ от модели: {raw}")

    # ✨ Формируем API-ответ в нужной структуре
    return {
        "name": "Meal",
        "calories": f"{raw} kcal",
        "description": "Автоматически распознанный приём пищи по изображению.",
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
