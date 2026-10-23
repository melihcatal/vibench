from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _clean_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()


def _list_from_value(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [_clean_text(item) for item in value if _clean_text(item)]
    if isinstance(value, str):
        pieces = [piece.strip() for piece in value.replace(";", ",").split(",")]
        return [piece for piece in pieces if piece]
    return [_clean_text(value)] if _clean_text(value) else []


@dataclass
class VisionRequest:
    image_path: str
    prompt: str = ""
    language: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        payload = {"image_path": self.image_path, "prompt": self.prompt}
        if self.language:
            payload["language"] = self.language
        if self.extra:
            payload.update(self.extra)
        return payload


@dataclass
class VisionResult:
    labels: List[str] = field(default_factory=list)
    description: str = ""
    text: List[str] = field(default_factory=list)
    unsafe: bool = False
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "VisionResult":
        return cls(
            labels=_list_from_value(payload.get("labels") or payload.get("objects") or payload.get("tags")),
            description=_clean_text(payload.get("description") or payload.get("caption") or payload.get("summary")),
            text=_list_from_value(payload.get("text") or payload.get("ocr") or payload.get("detected_text")),
            unsafe=bool(payload.get("unsafe") or payload.get("policy_flagged") or payload.get("is_unsafe")),
            raw=payload,
        )


def normalize_labels(items: Any) -> List[str]:
    return _list_from_value(items)


def normalize_text(items: Any) -> List[str]:
    return _list_from_value(items)
