import base64
import re
from openai import OpenAI

# ⚠️ API-ключ вставляется прямо сюда
OPENAI_API_KEY = "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"

# 📡 Создаём OpenAI клиент напрямую
client = OpenAI(api_key=OPENAI_API_KEY)

def query_openai_image(image_bytes: bytes):
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "На фото изображена еда. Верни JSON: { \"name\": ..., \"calories\": ..., \"description\": ... }"
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
    name_match = re.search(r'"name"\s*:\s*"([^"]+)"', text)
    calories_match = re.search(r'"calories"\s*:\s*"([^"]+)"', text)
    description_match = re.search(r'"description"\s*:\s*"([^"]+)"', text)

    return {
        "name": name_match.group(1) if name_match else "Unknown",
        "calories": calories_match.group(1) if calories_match else "N/A",
        "description": description_match.group(1) if description_match else text.strip()
    }
