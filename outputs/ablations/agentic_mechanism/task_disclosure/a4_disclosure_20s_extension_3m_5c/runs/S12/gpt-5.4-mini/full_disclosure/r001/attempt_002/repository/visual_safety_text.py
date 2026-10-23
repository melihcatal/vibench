import json
import os
from typing import Any, Dict, List, Optional

import requests


OPENAI_VISION_MODEL = os.getenv("OPENAI_VISION_MODEL", "gpt-4.1-mini")
OPENAI_RESPONSES_API_URL = os.getenv("OPENAI_RESPONSES_API_URL", "https://api.openai.com/v1/responses")


def _get_api_key(api_key: Optional[str] = None) -> str:
    key = api_key or os.getenv("OPENAI_API_KEY")
    if not key:
        raise ValueError("OPENAI_API_KEY is required")
    return key


def _coerce_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, dict):
        for key in ("text", "value", "content", "label", "rationale"):
            if key in value:
                return _coerce_text(value[key])
        return ""
    if isinstance(value, list):
        parts = [_coerce_text(item) for item in value]
        return "\n".join(part for part in parts if part)
    return str(value).strip()


def _coerce_str_list(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, str):
        text = value.strip()
        return [text] if text else []
    if isinstance(value, dict):
        for key in ("items", "labels", "categories", "values"):
            if key in value:
                return _coerce_str_list(value[key])
        text = _coerce_text(value)
        return [text] if text else []
    if isinstance(value, list):
        result: List[str] = []
        for item in value:
            text = _coerce_text(item)
            if text:
                result.append(text)
        return result
    text = _coerce_text(value)
    return [text] if text else []


def _normalize_result(value: Any) -> Dict[str, Any]:
    if isinstance(value, dict):
        unsafe = bool(value.get("unsafe", False))
        severity = _coerce_text(value.get("severity")) or "low"
        categories = _coerce_str_list(value.get("categories"))
        rationale = _coerce_text(value.get("rationale") or value.get("text") or value.get("content"))
        return {"unsafe": unsafe, "severity": severity, "categories": categories, "rationale": rationale}
    text = _coerce_text(value)
    return {"unsafe": False, "severity": "low", "categories": [], "rationale": text}


def _extract_output_text(data: Dict[str, Any]) -> str:
    parts: List[str] = []
    for item in data.get("output", []):
        for content in item.get("content", []):
            if content.get("type") in {"output_text", "text"}:
                parts.append(content.get("text", ""))
    return "".join(parts).strip()


def check_visual_safety_text(labels: Any, api_key: Optional[str] = None, model: Optional[str] = None, timeout: int = 60) -> Dict[str, Any]:
    key = _get_api_key(api_key)
    model_name = model or OPENAI_VISION_MODEL
    labels_text = _coerce_text(labels)
    payload = {
        "model": model_name,
        "input": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": "Check these generated visual labels for unsafe, offensive, sexual, violent, hateful, or otherwise policy-sensitive text. Return only JSON with keys unsafe (boolean), severity (one of low, medium, high), categories (array of strings), and rationale (string). Labels:\n" + labels_text,
                    }
                ],
            }
        ],
        "max_output_tokens": 200,
    }
    response = requests.post(
        OPENAI_RESPONSES_API_URL,
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=timeout,
    )
    response.raise_for_status()
    data = response.json()
    text = _extract_output_text(data)
    try:
        parsed = json.loads(text)
        return _normalize_result(parsed)
    except json.JSONDecodeError:
        return _normalize_result(text)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: python visual_safety_text.py LABELS_JSON_OR_TEXT")
    print(json.dumps(check_visual_safety_text(sys.argv[1]), ensure_ascii=False))
