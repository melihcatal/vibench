import os
from openai import OpenAI
from typing import Dict, Any

def moderate_profile_text(text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = OpenAI(api_key=api_key)
    response = client.moderations.create(input=text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores)
    }