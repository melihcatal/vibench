import os
from openai import OpenAI
from typing import Dict


def check_safety(script: str) -> Dict:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        input=script, model="text-moderation-3.5-2024-04-09"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }
