import os
from openai import OpenAI
from typing import Dict, Any

def check_payload_safety(payload: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(model="text-moderation-latest", input=payload)
    result = response.results[0]
    return {
        "is_safe": not result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }