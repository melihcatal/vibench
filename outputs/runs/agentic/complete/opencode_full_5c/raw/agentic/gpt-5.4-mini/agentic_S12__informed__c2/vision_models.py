from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class VisionRequest:
    image_path: str
    prompt: Optional[str] = None
    language: Optional[str] = None


@dataclass
class VisionResult:
    provider: str
    data: Dict[str, Any]


def normalize_labels(payload: Any) -> List[str]:
    labels = []
    if isinstance(payload, dict):
        for key in ("labels", "tags", "objects", "categories"):
            value = payload.get(key)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str):
                        labels.append(item)
                    elif isinstance(item, dict):
                        name = (
                            item.get("name")
                            or item.get("description")
                            or item.get("text")
                        )
                        if name:
                            labels.append(str(name))
    return labels


def normalize_text(payload: Any) -> str:
    if isinstance(payload, dict):
        for key in ("text", "fullText", "recognizedText", "content"):
            value = payload.get(key)
            if isinstance(value, str):
                return value
    return ""


def normalize_safety(payload: Any) -> Dict[str, Any]:
    if isinstance(payload, dict):
        return payload
    return {"result": payload}
