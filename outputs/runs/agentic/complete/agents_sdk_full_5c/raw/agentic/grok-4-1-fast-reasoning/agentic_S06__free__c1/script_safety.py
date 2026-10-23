import os
from openai import OpenAI
from typing import Dict, Any

def check_safety(script: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(
        input=script,
        model="text-moderation-latest"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores
    }
