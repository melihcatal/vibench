from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def _norm_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


@dataclass
class TextSafetyRequest:
    text: str
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_input(cls, value: Any) -> "TextSafetyRequest":
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(
                text=_norm_text(value.get("text") or value.get("input")),
                user_id=value.get("user_id"),
                metadata=value.get("metadata"),
            )
        return cls(text=_norm_text(value))


@dataclass
class BatchTextSafetyRequest:
    messages: List[str]
    user_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_input(cls, value: Any) -> "BatchTextSafetyRequest":
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            raw = value.get("messages") or value.get("texts") or []
            return cls(
                messages=[_norm_text(v) for v in raw],
                user_id=value.get("user_id"),
                metadata=value.get("metadata"),
            )
        return cls(messages=[_norm_text(v) for v in value])


@dataclass
class SafetyThresholds:
    violence: float = 0.5
    self_harm: float = 0.5
    sexual: float = 0.5
    hate: float = 0.5
    harassment: float = 0.5

    @classmethod
    def from_input(cls, value: Any) -> "SafetyThresholds":
        if isinstance(value, cls):
            return value
        if isinstance(value, dict):
            return cls(
                **{
                    k: float(value[k])
                    for k in ["violence", "self_harm", "sexual", "hate", "harassment"]
                    if k in value
                }
            )
        return cls()


def normalize_spans(spans: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for span in spans or []:
        if not isinstance(span, dict):
            continue
        out.append(
            {
                "start": int(span.get("start", 0)),
                "end": int(span.get("end", 0)),
                "label": _norm_text(span.get("label") or span.get("category")),
            }
        )
    return out
