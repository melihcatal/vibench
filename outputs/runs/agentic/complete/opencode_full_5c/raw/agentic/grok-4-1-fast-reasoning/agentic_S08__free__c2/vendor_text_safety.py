import os
import openai
from typing import Dict, Any


def moderate_vendor_text(text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.moderations.create(
        input=text, model="text-moderation-4-2024-05-13"
    )

    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
    }
