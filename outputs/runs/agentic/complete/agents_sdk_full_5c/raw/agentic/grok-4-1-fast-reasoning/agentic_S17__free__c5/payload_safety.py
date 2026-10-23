from openai import OpenAI
import os
from typing import Dict, Any

def check_payload_safety(payload: str) -> Dict[str, Any]:
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    moderation = client.moderations.create(
        model="text-moderation-latest",
        input=payload
    )
    result = moderation.results[0]
    return {
        'safe': not result.flagged,
        'categories': dict(result.categories),
        'category_scores': dict(result.category_scores)
    }