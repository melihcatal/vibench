from typing import Any, Dict
import os
from openai import OpenAI
from safety_models import normalize_text_input, build_text_moderation_result
from safety_client import get_openai_client, get_moderation_model_name


def moderate_text(text: str, *, model: str | None = None) -> Dict[str, Any]:
    client = get_openai_client()
    payload = normalize_text_input(text)
    model_name = model or get_moderation_model_name()
    response = client.moderations.create(model=model_name, input=payload["text"])
    result = response.results[0]
    return build_text_moderation_result(
        text=payload["text"],
        flagged=bool(result.flagged),
        categories=dict(result.categories),
        category_scores=dict(result.category_scores),
        model=model_name,
    )


if __name__ == "__main__":
    raise SystemExit(0)
