import os
from typing import Dict, Any
from messaging_client import get_openai_client

def check_message_safety(text_content: str) -> Dict[str, Any]:
    openai_client = get_openai_client()
    try:
        response = openai_client.moderations.create(input=text_content)
        result = response.results[0]
        return {
            "flagged": result.flagged,
            "categories": {k: v for k, v in result.categories.model_dump().items() if v},
            "category_scores": result.category_scores.model_dump()
        }
    except Exception as e:
        return {"error": str(e), "flagged": True, "details": "Could not perform safety check."}