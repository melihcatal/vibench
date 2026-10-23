from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _text(obj: Any) -> str:
    if obj is None:
        return ""
    if isinstance(obj, str):
        return obj
    for attr in ("content", "text", "value"):
        if hasattr(obj, attr):
            v = getattr(obj, attr)
            if isinstance(v, str):
                return v
    return str(obj)


def normalize_payload(payload: Any) -> Dict[str, Any]:
    if payload is None:
        return {}
    if isinstance(payload, dict):
        return payload
    if hasattr(payload, "to_dict"):
        try:
            value = payload.to_dict()
            if isinstance(value, dict):
                return value
        except Exception:
            pass
    if hasattr(payload, "as_dict"):
        try:
            value = payload.as_dict()
            if isinstance(value, dict):
                return value
        except Exception:
            pass
    return {"raw": _text(payload)}


def normalize_lines(payload: Any) -> List[str]:
    data = normalize_payload(payload)
    if "lines" in data and isinstance(data["lines"], list):
        return [_text(item) for item in data["lines"]]
    return []


def normalize_tables(payload: Any) -> List[Dict[str, Any]]:
    data = normalize_payload(payload)
    if "tables" in data and isinstance(data["tables"], list):
        return [normalize_payload(item) for item in data["tables"]]
    return []


def normalize_key_values(payload: Any) -> Dict[str, str]:
    data = normalize_payload(payload)
    kv = data.get("key_values") or data.get("keyValuePairs") or []
    result: Dict[str, str] = {}
    if isinstance(kv, list):
        for item in kv:
            item_data = normalize_payload(item)
            key = _text(
                item_data.get("key") or item_data.get("name") or item_data.get("field")
            )
            value = _text(item_data.get("value") or item_data.get("content"))
            if key:
                result[key] = value
    return result


@dataclass
class OCRRequest:
    image_url: Optional[str] = None
    image_bytes: Optional[bytes] = None
    language: Optional[str] = None
    locale: Optional[str] = None
    features: List[str] = field(default_factory=list)


@dataclass
class OCRResponse:
    text: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LayoutResponse:
    blocks: List[Dict[str, Any]] = field(default_factory=list)
    lines: List[str] = field(default_factory=list)
    tables: List[Dict[str, Any]] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)
