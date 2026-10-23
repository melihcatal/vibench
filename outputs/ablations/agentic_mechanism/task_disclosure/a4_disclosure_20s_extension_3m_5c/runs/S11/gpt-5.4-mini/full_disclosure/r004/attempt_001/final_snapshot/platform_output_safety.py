import os
from typing import Any, Dict, Optional

from openai import OpenAI


DEFAULT_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def check_platform_output_safety(output: str, model: str = DEFAULT_MODEL) -> Dict[str, Any]:
    client = _client()
    result = client.moderations.create(model=model, input=output)
    item = result.results[0]
    categories = getattr(item, "categories", None)
    category_scores = getattr(item, "category_scores", None)
    flagged = bool(getattr(item, "flagged", False))
    return {
        "provider": "openai",
        "model": model,
        "flagged": flagged,
        "categories": categories.model_dump() if hasattr(categories, "model_dump") else categories,
        "category_scores": category_scores.model_dump() if hasattr(category_scores, "model_dump") else category_scores,
        "raw": result.model_dump() if hasattr(result, "model_dump") else result,
    }


def is_platform_output_safe(output: str, model: str = DEFAULT_MODEL) -> bool:
    return not check_platform_output_safety(output, model=model)["flagged"]
