import os
from typing import Any, Dict, Optional

from openai import OpenAI


def check_platform_output_safety(output_text: str, model: Optional[str] = None) -> Dict[str, Any]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    safety_model = model or os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest")
    response = client.moderations.create(model=safety_model, input=output_text)
    result = response.results[0]
    categories = dict(result.categories)
    category_scores = dict(result.category_scores)
    unsafe = bool(result.flagged or any(categories.values()))
    return {
        "provider": "openai",
        "model": safety_model,
        "unsafe": unsafe,
        "flagged": bool(result.flagged),
        "categories": categories,
        "category_scores": category_scores,
        "raw_response": response.model_dump() if hasattr(response, "model_dump") else response,
    }
