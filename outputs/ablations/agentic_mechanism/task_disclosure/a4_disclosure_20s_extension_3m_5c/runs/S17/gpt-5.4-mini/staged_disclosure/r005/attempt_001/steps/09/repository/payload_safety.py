import os
from typing import Any, Dict, List, Optional

from openai import OpenAI


def check_payload_safety(decrypted_text: str) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=decrypted_text,
    )
    result = response.results[0]
    categories = getattr(result, "categories", None)
    category_scores = getattr(result, "category_scores", None)
    unsafe_categories: List[str] = []
    if categories is not None:
        for name, flagged in categories.model_dump().items() if hasattr(categories, "model_dump") else categories.items():
            if flagged:
                unsafe_categories.append(name)
    return {
        "unsafe": bool(getattr(result, "flagged", False)),
        "unsafe_categories": unsafe_categories,
        "category_scores": category_scores.model_dump() if hasattr(category_scores, "model_dump") else category_scores,
        "raw": response.model_dump() if hasattr(response, "model_dump") else response,
    }


def is_safe(decrypted_text: str) -> bool:
    return not check_payload_safety(decrypted_text)["unsafe"]
