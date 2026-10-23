import json
import os
from typing import Any, Dict, List

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def check_message_safety(payload_text: str) -> Dict[str, Any]:
    client = _client()
    response = client.responses.create(
        model="omni-moderation-latest",
        input=payload_text,
    )
    output = response.output_text if hasattr(response, "output_text") else ""
    verdict = {"safe": True, "categories": [], "raw": output}
    try:
        parsed = json.loads(output) if output else {}
        if isinstance(parsed, dict):
            verdict.update(parsed)
    except Exception:
        pass
    return verdict


def is_message_safe(payload_text: str) -> bool:
    result = check_message_safety(payload_text)
    return bool(result.get("safe", True))
