from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class DocumentExtractionRequest:
    file_path: Optional[str] = None
    content: Optional[bytes] = None
    locale: Optional[str] = None


@dataclass
class DocumentExtractionResponse:
    provider: str
    fields: Dict[str, Any]
    raw: Any


def normalize_confidence(value: Any) -> float:
    try:
        return max(0.0, min(1.0, float(value)))
    except Exception:
        return 0.0


def as_line_items(items: Any) -> List[Dict[str, Any]]:
    if not items:
        return []
    result = []
    for item in items:
        if isinstance(item, dict):
            result.append(item)
        else:
            result.append({"value": item})
    return result
