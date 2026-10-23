import os
from openai import OpenAI
from typing import Dict, Any


def ocr_safety(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(input=text, model="text-moderation-latest")
    result = response.results[0]
    return {
        "is_safe": not result.flagged,
        "flagged_categories": result.categories,
        "category_scores": result.category_scores,
    }
