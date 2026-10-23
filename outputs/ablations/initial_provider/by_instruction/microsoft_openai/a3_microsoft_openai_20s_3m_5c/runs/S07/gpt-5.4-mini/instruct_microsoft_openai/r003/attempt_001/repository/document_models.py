from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentRequest:
    image_path: Optional[str] = None
    image_b64: Optional[str] = None
    prompt: str = ""


@dataclass
class DocumentResponse:
    text: str
    raw: Any


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        return "\n".join(normalize_text(v) for v in value if normalize_text(v))
    if isinstance(value, dict):
        if "text" in value:
            return normalize_text(value["text"])
        return " ".join(f"{k}: {normalize_text(v)}" for k, v in value.items() if normalize_text(v))
    return str(value).strip()


def normalize_key_values(items: List[Dict[str, Any]]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for item in items:
        key = normalize_text(item.get("key"))
        value = normalize_text(item.get("value"))
        if key:
            result[key] = value
    return result
