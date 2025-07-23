from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import datetime
from openai_api import query_openai_image, parse_response_to_structured_format

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-meal")
async def analyze_meal(file: UploadFile = File(...)):
    print(f"📥 Получен файл: {file.filename}")

    image_bytes = await file.read()
    response_text = query_openai_image(image_bytes)
    structured = parse_response_to_structured_format(response_text)

    structured["timestamp"] = datetime.datetime.utcnow().isoformat()
    return structured
