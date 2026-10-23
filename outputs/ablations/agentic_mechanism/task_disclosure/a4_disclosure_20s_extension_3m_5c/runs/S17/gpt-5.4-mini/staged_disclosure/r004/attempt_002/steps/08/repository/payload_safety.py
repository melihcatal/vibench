import json
import os
from typing import Any, Dict, Optional

import openai


class PayloadSafetyError(ValueError):
    pass


def _client() -> openai.OpenAI:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise PayloadSafetyError("OPENAI_API_KEY is required")
    return openai.OpenAI(api_key=api_key)


def _extract_text(response: Any) -> str:
    if hasattr(response, "output_text") and response.output_text:
        return str(response.output_text)
    try:
        return json.dumps(response.model_dump() if hasattr(response, "model_dump") else response)
    except Exception:
        return str(response)


def check_decrypted_payload(payload: str, model: str = "gpt-4.1-mini") -> Dict[str, Any]:
    if not isinstance(payload, str) or not payload.strip():
        raise PayloadSafetyError("payload must be a non-empty string")

    client = _client()
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "system",
                "content": "Classify decrypted text payloads for unsafe content. Return strict JSON with keys unsafe (boolean), category (string), reason (string), and confidence (number from 0 to 1).",
            },
            {"role": "user", "content": payload},
        ],
        temperature=0,
    )
    text = _extract_text(response).strip()
    try:
        result = json.loads(text)
    except json.JSONDecodeError:
        result = {"unsafe": True, "category": "unparseable", "reason": text, "confidence": 0.0}

    if not isinstance(result, dict):
        raise PayloadSafetyError("unexpected provider response")
    result.setdefault("unsafe", False)
    result.setdefault("category", "unknown")
    result.setdefault("reason", "")
    result.setdefault("confidence", 0.0)
    return result
