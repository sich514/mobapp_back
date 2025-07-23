import openai
import base64
import os
import re
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def query_openai_image(image_bytes: bytes) -> str:
    """
    Отправляет изображение в OpenAI GPT-4 Vision и возвращает текстовый ответ.
    """
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = openai.ChatCompletion.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "На фото изображена еда. Проанализируй и верни JSON-объект строго в формате:\n"
                            "{ \"name\": название блюда, \"calories\": калорийность, \"description\": описание еды }"
                        )
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        max_tokens=500
    )

    return response.choices[0].message.content

def parse_response_to_structured_format(text: str) -> dict:
    """
    Пытается извлечь структурированные данные из текстового или JSON-подобного ответа.
    """
    # Пытаемся найти JSON-подобную структуру в ответе
    name_match = re.search(r'"name"\s*:\s*"([^"]+)"', text)
    calories_match = re.search(r'"calories"\s*:\s*"([^"]+)"', text)
    description_match = re.search(r'"description"\s*:\s*"([^"]+)"', text)

    return {
        "name": name_match.group(1) if name_match else "Unknown",
        "calories": calories_match.group(1) if calories_match else "N/A",
        "description": description_match.group(1) if description_match else text.strip()
    }
