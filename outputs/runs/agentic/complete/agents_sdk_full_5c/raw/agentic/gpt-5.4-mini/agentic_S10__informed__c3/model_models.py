from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import json


@dataclass
class TextRequest:
    prompt: str
    model: Optional[str] = None
    temperature: Optional[float] = None


@dataclass
class TextResponse:
    text: str
    model: Optional[str] = None
    raw: Optional[Any] = None


@dataclass
class JsonExtraction:
    data: Dict[str, Any]
    raw_text: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if isinstance(value, list):
        parts: List[str] = []
        for item in value:
            if isinstance(item, dict) and "text" in item:
                parts.append(str(item["text"]))
            else:
                parts.append(str(item))
        return "".join(parts).strip()
    if isinstance(value, dict):
        for key in ("content", "text", "output_text"):
            if key in value:
                return normalize_text(value[key])
    return str(value).strip()


def safe_json_loads(text: str) -> Dict[str, Any]:
    try:
        loaded = json.loads(text)
        if isinstance(loaded, dict):
            return loaded
        return {"value": loaded}
    except Exception:
        return {"raw": text}
