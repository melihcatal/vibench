import os
import openai
from typing import Dict, Any


def check_platform_output_safety(text: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation = client.moderations.create(input=text)
    result = moderation.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
