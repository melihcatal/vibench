import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_HOST = "https://api.openai.com/v1"
OPENAI_MODEL = "gpt-4.1-mini"


def check_unsafe_copy(text: str, locale: Optional[str] = None) -> Dict[str, Any]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    prompt = {
        "role": "user",
        "content": (
            "Assess the following localized copy for unsafe content. "
            "Return JSON with keys: unsafe (boolean), categories (array of strings), "
            "issues (array of strings), and summary (string). "
            f"Locale: {locale or 'unknown'}\nText: {text}"
        ),
    }

    response = requests.post(
        f"{OPENAI_API_HOST}/responses",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "input": [prompt],
            "temperature": 0,
        },
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    output_text = _extract_output_text(data)
    return _parse_json_result(output_text)


def _extract_output_text(payload: Dict[str, Any]) -> str:
    if "output_text" in payload and isinstance(payload["output_text"], str):
        return payload["output_text"]
    parts: List[str] = []
    for item in payload.get("output", []):
        for content in item.get("content", []):
            text = content.get("text")
            if isinstance(text, str):
                parts.append(text)
    if parts:
        return "\n".join(parts)
    raise RuntimeError("Unexpected response format from OpenAI Responses API")


def _parse_json_result(text: str) -> Dict[str, Any]:
    import json

    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise RuntimeError("Model did not return JSON")
    return json.loads(text[start : end + 1])
