import base64
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


def image_bytes_to_data_uri(image_bytes: bytes, mime_type: str = 'image/jpeg') -> str:
    return f"data:{mime_type};base64,{base64.b64encode(image_bytes).decode('ascii')}"


def normalize_labels(items: Any) -> List[str]:
    if not items:
        return []
    if isinstance(items, dict):
        items = items.get('labels') or items.get('items') or items.get('predictions') or []
    out = []
    for item in items:
        if isinstance(item, str):
            out.append(item)
        elif isinstance(item, dict):
            out.append(str(item.get('name') or item.get('label') or item.get('text') or item.get('value') or ''))
    return [x for x in out if x]


def normalize_text(items: Any) -> str:
    if not items:
        return ''
    if isinstance(items, str):
        return items
    if isinstance(items, dict):
        for key in ('text', 'description', 'result'):
            if key in items and items[key]:
                return str(items[key])
        return ' '.join(normalize_labels(items))
    if isinstance(items, list):
        return ' '.join(normalize_labels(items))
    return str(items)


def normalize_safety(items: Any) -> Dict[str, Any]:
    if isinstance(items, dict):
        return items
    return {'unsafe': bool(items)}
