import json
from typing import Any


def _extract_content(payload: Any) -> str:
    if isinstance(payload, dict):
        choices = payload.get('choices') or []
        if choices:
            message = choices[0].get('message') or {}
            content = message.get('content')
            if isinstance(content, str):
                return content
            if isinstance(content, list):
                return ''.join(part.get('text', '') for part in content if isinstance(part, dict))
        return str(payload)
    return str(payload)


def normalize_text_response(payload: Any) -> str:
    return _extract_content(payload).strip()


def normalize_labels_response(payload: Any):
    text = _extract_content(payload).strip()
    return [item.strip() for item in text.replace('
', ',').split(',') if item.strip()]


def normalize_safety_response(payload: Any):
    text = _extract_content(payload).strip()
    try:
        return json.loads(text)
    except Exception:
        return {'verdict': text}
