import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def moderate_batch(messages: List[str]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for message in messages:
        response = client.moderations.create(
            model="omni-moderation-latest",
            input=message,
        )
        result = response.results[0]
        categories = getattr(result, "categories", {})
        category_scores = getattr(result, "category_scores", {})
        results.append(
            {
                "message": message,
                "flagged": bool(result.flagged),
                "categories": categories.model_dump() if hasattr(categories, "model_dump") else dict(categories),
                "category_scores": category_scores.model_dump() if hasattr(category_scores, "model_dump") else dict(category_scores),
            }
        )
    return results


def handle_batch(messages: List[str]) -> List[Dict[str, Any]]:
    return moderate_batch(messages)
