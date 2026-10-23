import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_MODERATION_API_URL = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"


def _extract_text(message_payload: Any) -> str:
    if isinstance(message_payload, str):
        return message_payload
    if isinstance(message_payload, dict):
        for key in ("text", "content", "message", "body", "payload"):
            value = message_payload.get(key)
            if isinstance(value, str):
                return value
            if isinstance(value, list):
                parts: List[str] = []
                for item in value:
                    if isinstance(item, str):
                        parts.append(item)
                    elif isinstance(item, dict):
                        text = item.get("text") or item.get("content")
                        if isinstance(text, str):
                            parts.append(text)
                if parts:
                    return "\n".join(parts)
    return ""


def check_message_payload_text_for_unsafe_content(message_payload: Any) -> Dict[str, Any]:
    text = _extract_text(message_payload)
    if not text:
        return {"safe": True, "flagged": False, "categories": {}, "category_scores": {}, "provider": "openai"}

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required for OpenAI Moderation API")

    response = requests.post(
        OPENAI_MODERATION_API_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={"model": OPENAI_MODERATION_MODEL, "input": text},
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    result = data["results"][0]
    flagged = bool(result.get("flagged"))
    categories = result.get("categories", {})
    category_scores = result.get("category_scores", {})
    return {
        "safe": not flagged,
        "flagged": flagged,
        "categories": categories,
        "category_scores": category_scores,
        "provider": "openai",
    }
