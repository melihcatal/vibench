from __future__ import annotations

from typing import Dict

from observability_client import openai_post


def log_text_safety(message: str) -> Dict[str, object]:
    response = openai_post(
        "moderations",
        {
            "model": "omni-moderation-latest",
            "input": message,
        },
    )
    result = response["results"][0]
    return {
        "flagged": result["flagged"],
        "categories": result["categories"],
        "category_scores": result["category_scores"],
    }
