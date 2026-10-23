from __future__ import annotations

import os
from typing import Any, Dict

from safety_client import get_anthropic_client, safety_model_name
from safety_models import ModerationRequest, ModerationResult, normalize_moderation_response


MODERATION_SYSTEM_PROMPT = """You are a strict text content safety classifier.\nReturn JSON only with keys: allowed (bool), categories (object), reasons (array of strings), redactions (array of objects).\nClassify violence, self-harm, hate, sexual content, harassment, fraud, and illegal content.\n"""


def moderate_text(text: str, user_id: str | None = None) -> ModerationResult:
    request = ModerationRequest(text=text, user_id=user_id)
    client = get_anthropic_client()
    response = client.messages.create(  # anthropic SDK
        model=safety_model_name("moderation"),
        max_tokens=600,
        temperature=0,
        system=MODERATION_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": request.to_prompt(),
            }
        ],
    )
    return normalize_moderation_response(response)


if __name__ == "__main__":
    sample = os.environ.get("SAFETY_SAMPLE_TEXT", "")
    if sample:
        result = moderate_text(sample)
        print(result.model_dump_json())
