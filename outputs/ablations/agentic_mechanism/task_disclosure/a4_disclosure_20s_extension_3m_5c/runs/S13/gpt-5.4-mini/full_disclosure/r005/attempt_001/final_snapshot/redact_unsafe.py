import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


def _headers() -> Dict[str, str]:
    api_key = os.environ["OPENAI_API_KEY"]
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _request_payload(text: str, mode: str = "redact") -> Dict[str, Any]:
    system = (
        "You are a moderation assistant. Identify unsafe spans in the input text and either "
        "flag them with indices or return a redacted version. Respond with JSON only."
    )
    user = {
        "text": text,
        "mode": mode,
        "output_schema": {
            "unsafe_spans": [{"start": 0, "end": 0, "category": "string", "reason": "string"}],
            "redacted_text": "string",
            "is_safe": True,
        },
    }
    return {
        "model": OPENAI_MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": str(user)},
        ],
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }


def redact_unsafe(text: str, mode: str = "redact", timeout: int = 30) -> Dict[str, Any]:
    response = requests.post(
        OPENAI_API_URL,
        headers=_headers(),
        json=_request_payload(text, mode),
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    content = data["choices"][0]["message"]["content"]
    if isinstance(content, str):
        import json

        return json.loads(content)
    return content


def flag_unsafe_spans(text: str, timeout: int = 30) -> List[Dict[str, Any]]:
    result = redact_unsafe(text, mode="flag", timeout=timeout)
    return result.get("unsafe_spans", [])


def redact_text(text: str, timeout: int = 30) -> str:
    result = redact_unsafe(text, mode="redact", timeout=timeout)
    return result.get("redacted_text", text)
