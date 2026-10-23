import openai
import os
from typing import Dict, Any

def check_annotation_safety(text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="text-moderation-4-2024-10-29",
        input=text
    )
    return {
        "flagged": response.results[0].flagged,
        "categories": response.results[0].categories,
        "category_scores": response.results[0].category_scores
    }