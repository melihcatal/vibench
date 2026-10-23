from typing import Any, Dict

from openai import OpenAI

from model_client import get_openai_client, get_model_name


def platform_output_safety(text: str) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    model = get_model_name(default="gpt-4.1-mini")
    moderation = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )
    result = moderation.results[0]
    return {
        "provider": "openai",
        "model": model,
        "flagged": bool(result.flagged),
        "categories": getattr(result, "categories", None),
        "category_scores": getattr(result, "category_scores", None),
        "moderation_id": getattr(moderation, "id", None),
    }
