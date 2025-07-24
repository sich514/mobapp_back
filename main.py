from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import datetime
import base64
from PIL import Image
import io
from openai import OpenAI
import os

# 🔐 Твой API-ключ
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print('Yes')

app = FastAPI()

# ✅ CORS: разрешаем запросы из FlutterFlow
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # можно ограничить при необходимости
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_to_jpeg(image_bytes: bytes) -> bytes:
    """Приводим изображение к JPEG для гарантированной совместимости с OpenAI"""
    try:
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        buffer = io.BytesIO()
        image.save(buffer, format="JPEG")
        return buffer.getvalue()
    except Exception as e:
        raise RuntimeError(f"Ошибка обработки изображения: {e}")

def encode_image_for_openai(image_bytes: bytes) -> str:
    """Создаём base64 URL-строку"""
    return f"data:image/jpeg;base64,{base64.b64encode(image_bytes).decode('utf-8')}"

@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    print(f"📥 Получен файл: {file.filename} (MIME: {file.content_type})")

    try:
        original_bytes = await file.read()

        # Преобразуем всё к JPEG
        jpeg_bytes = convert_to_jpeg(original_bytes)

        # Кодируем в base64 для запроса
        image_url = encode_image_for_openai(jpeg_bytes)

        # 📡 Отправляем в OpenAI (model gpt-4.1)
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
                            "image_url": image_url,
                        }
                    ]
                }
            ]
        )

        raw_text = response.output_text.strip()
        print(f"🎯 Получен ответ: {raw_text}")

        return {
            "name": "Meal",
            "calories": f"{raw_text} kcal",
            "description": "Автоматически рассчитанная калорийность по изображению",
            "timestamp": datetime.datetime.utcnow().isoformat()
        }

    except Exception as e:
        print(f"❌ Ошибка обработки запроса: {e}")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
