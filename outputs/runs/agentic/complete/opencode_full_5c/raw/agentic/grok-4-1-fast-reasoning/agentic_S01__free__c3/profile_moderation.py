import os
from openai import OpenAI
from typing import Dict, Any


def moderate_profile_text(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    moderation = client.moderations.create(
        input=text,
        model="text-moderation-latest",
    )
    result = moderation.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
