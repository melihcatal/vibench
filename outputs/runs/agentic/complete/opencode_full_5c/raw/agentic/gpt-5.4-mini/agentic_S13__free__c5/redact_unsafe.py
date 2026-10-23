import os
from typing import Any, Dict

from openai import OpenAI

from safety_client import get_openai_client, normalize_text_input


def redact_unsafe(text: Any) -> Dict[str, Any]:
    client: OpenAI = get_openai_client()
    response = client.moderations.create(
        model=os.environ.get("OPENAI_MODERATION_MODEL", "omni-moderation-latest"),
        input=normalize_text_input(text),
    )
    result = response.results[0]
    redacted = normalize_text_input(text)
    if result.flagged:
        redacted = "[REDACTED]"
    return {
        "flagged": bool(result.flagged),
        "redacted_text": redacted,
        "categories": dict(result.categories),
    }
