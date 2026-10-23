import openai
import os
from typing import Dict, Any

def check_payload_safety(payload: str) -> Dict[str, Any]:
    client = openai.OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    response = client.moderations.create(
        input=payload,
        model="text-moderation-latest"
    )
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores
    }