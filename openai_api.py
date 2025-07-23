import re

def parse_response_to_structured_format(text: str):
    # Наивный парсинг — можно улучшить при необходимости
    name_match = re.search(r"(?:Блюдо:|Название:|Name:)\s*(.+)", text)
    calories_match = re.search(r"(?:Калории:|Calories:)\s*(.+)", text)
    description_match = re.search(r"(?:Описание:|Description:)\s*(.+)", text)

    return {
        "name": name_match.group(1).strip() if name_match else "Unknown",
        "calories": calories_match.group(1).strip() if calories_match else "N/A",
        "description": description_match.group(1).strip() if description_match else text.strip()
    }
