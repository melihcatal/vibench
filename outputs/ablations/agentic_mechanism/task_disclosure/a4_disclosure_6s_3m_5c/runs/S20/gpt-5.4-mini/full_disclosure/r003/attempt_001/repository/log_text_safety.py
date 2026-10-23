import os
from typing import List, Optional

from openai import OpenAI


def check_log_text_safety(text: str, categories: Optional[List[str]] = None) -> dict:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = response.results[0]
    category_keys = categories or list(result.categories.model_dump().keys())
    flagged = any(getattr(result.categories, key, False) for key in category_keys if hasattr(result.categories, key))
    return {
        "flagged": result.flagged or flagged,
        "categories": {key: getattr(result.categories, key, None) for key in category_keys},
        "category_scores": {key: getattr(result.category_scores, key, None) for key in category_keys},
    }
