import os
from typing import Any, Dict

from openai import OpenAI

from safety_client import get_openai_client, moderation_model_name
from safety_models import normalize_moderation_result


def moderate_text(text: str, user_id: str | None = None) -> Dict[str, Any]:
    client = get_openai_client()
    model = moderation_model_name()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "You are a text safety moderation engine. Classify policy-violating, unsafe, or disallowed content in the user text and return structured JSON with categories, severity, and allow/deny decision.",
            },
            {
                "role": "user",
                "content": text,
            },
        ],
        text={"format": {"type": "json_object"}},
        metadata={"user_id": user_id} if user_id else None,
    )
    payload = response.output_text
    return normalize_moderation_result(payload)
