import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_RESPONSES_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = "gpt-4.1-mini"


def _build_prompt(text: str) -> str:
    return (
        "You are a document safety classifier. Evaluate the provided OCR text for unsafe content. "
        "Return strictly valid JSON with keys: unsafe (boolean), categories (array of strings), "
        "reason (string), confidence (number from 0 to 1). Classify as unsafe if the text contains "
        "violence, self-harm, sexual content involving minors, extremist content, fraud, malware, "
        "or other clearly harmful instructions. OCR text:\n\n"
        f"{text}"
    )


def _extract_output_text(response_json: Dict[str, Any]) -> str:
    output = response_json.get("output", [])
    parts: List[str] = []
    for item in output:
        content = item.get("content", []) if isinstance(item, dict) else []
        for segment in content:
            if isinstance(segment, dict):
                text = segment.get("text")
                if isinstance(text, str):
                    parts.append(text)
    if parts:
        return "".join(parts).strip()
    return str(response_json.get("output_text", "")).strip()


def check_ocr_safety(text: str, api_key: Optional[str] = None, timeout: int = 60) -> Dict[str, Any]:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": _build_prompt(text),
                    }
                ],
            }
        ],
        "text": {"format": {"type": "json_object"}},
    }
    response = requests.post(
        OPENAI_RESPONSES_API_URL,
        headers={
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    output_text = _extract_output_text(data)
    if output_text:
        try:
            import json

            return json.loads(output_text)
        except Exception:
            pass
    return data


def is_unsafe(text: str, api_key: Optional[str] = None, timeout: int = 60) -> bool:
    result = check_ocr_safety(text, api_key=api_key, timeout=timeout)
    return bool(result.get("unsafe", False))
