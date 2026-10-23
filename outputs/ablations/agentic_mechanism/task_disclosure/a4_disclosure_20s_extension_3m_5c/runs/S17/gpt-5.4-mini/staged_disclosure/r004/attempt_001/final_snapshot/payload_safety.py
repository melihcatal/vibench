import os
from typing import Any, Dict

from openai import OpenAI


def check_decrypted_payload(text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    categories = result.categories.model_dump() if hasattr(result.categories, "model_dump") else dict(result.categories)
    category_scores = result.category_scores.model_dump() if hasattr(result.category_scores, "model_dump") else dict(result.category_scores)
    unsafe = bool(result.flagged)
    return {
        "unsafe": unsafe,
        "provider": "openai",
        "model": "omni-moderation-latest",
        "categories": categories,
        "category_scores": category_scores,
    }


def is_payload_safe(text: str) -> bool:
    return not check_decrypted_payload(text)["unsafe"]
