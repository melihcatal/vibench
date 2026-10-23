import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _redact_spans(text: str, spans: List[Dict[str, Any]]) -> str:
    if not spans:
        return text
    chars = list(text)
    for span in spans:
        start = span.get("start")
        end = span.get("end")
        if isinstance(start, int) and isinstance(end, int) and 0 <= start < end <= len(chars):
            for i in range(start, end):
                chars[i] = "█"
    return "".join(chars)


def redact_unsafe(text: str, redact: bool = True, api_key: Optional[str] = None) -> Dict[str, Any]:
    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")

    payload = {"model": OPENAI_MODERATION_MODEL, "input": text}
    response = requests.post(
        OPENAI_MODERATION_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()

    results = data.get("results") or []
    if not results:
        return {"text": text, "flagged": False, "spans": [], "provider": "openai"}

    result = results[0]
    spans = result.get("categories", []) if isinstance(result.get("categories"), list) else []
    flagged = bool(result.get("flagged", False))
    unsafe_spans = result.get("spans") or []
    output_text = _redact_spans(text, unsafe_spans) if redact and flagged else text

    return {
        "text": output_text,
        "flagged": flagged,
        "spans": unsafe_spans,
        "categories": spans,
        "provider": "openai",
        "model": OPENAI_MODERATION_MODEL,
    }
