import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-5.4-mini"


def _extract_selected_text(log_message: Any) -> str:
    if isinstance(log_message, str):
        return log_message
    if isinstance(log_message, dict):
        for key in ("text", "message", "content", "log", "selected_text"):
            value = log_message.get(key)
            if isinstance(value, str) and value.strip():
                return value
        parts = []
        for value in log_message.values():
            if isinstance(value, str):
                parts.append(value)
        return " ".join(parts)
    return str(log_message)


def check_log_text_safety(log_message: Any, api_key: Optional[str] = None) -> Dict[str, Any]:
    text = _extract_selected_text(log_message)
    if not text.strip():
        return {"safe": True, "reason": "empty_text", "provider": "openai"}

    key = api_key or os.environ.get("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is required")

    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": [
                    {
                        "type": "text",
                        "text": "Classify the selected log message text for unsafe content. Return JSON with keys safe:boolean, reason:string, categories:list of strings, and confidence:number between 0 and 1.",
                    }
                ],
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": text,
                    }
                ],
            },
        ],
        "text": {"format": {"type": "json_object"}},
    }

    response = requests.post(OPENAI_API_URL, headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    data = response.json()

    output_text = ""
    for item in data.get("output", []):
        for content in item.get("content", []):
            if isinstance(content, dict) and content.get("type") in {"output_text", "text"}:
                output_text += content.get("text", "")

    if not output_text:
        output_text = data.get("output_text", "")

    import json

    try:
        result = json.loads(output_text)
    except Exception:
        result = {"safe": False, "reason": "unparseable_model_output", "raw": output_text}

    result["provider"] = "openai"
    return result
