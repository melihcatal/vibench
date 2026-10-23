import openai
import os
from typing import Dict, Any


def check_log_text_safety(log_text: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return {"flagged": False, "reason": "No API key provided"}
    client = openai.OpenAI(api_key=api_key)
    response = client.moderations.create(input=log_text)
    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": {k: float(v) for k, v in result.category_scores.items()},
    }
