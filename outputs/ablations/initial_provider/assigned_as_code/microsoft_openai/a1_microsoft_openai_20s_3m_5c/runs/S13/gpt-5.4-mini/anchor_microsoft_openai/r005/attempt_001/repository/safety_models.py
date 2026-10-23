from dataclasses import dataclass


def _text(value):
    return "" if value is None else str(value)


def _list_text(values):
    return [
        _text(value)
        for value in (values or [])
    ]


def _dict_text(values):
    return {str(key): values[key] for key in (values or {})}


@dataclass
class SafetyRequest:
    text: str
    metadata: dict | None = None

    @classmethod
    def from_payload(cls, payload):
        payload = payload or {}
        return cls(text=_text(payload.get("text")), metadata=_dict_text(payload.get("metadata")))


@dataclass
class SafetyBatchRequest:
    messages: list

    @classmethod
    def from_payload(cls, payload):
        payload = payload or {}
        return cls(messages=_list_text(payload.get("messages")))


@dataclass
class SafetyResponse:
    text: str
    score: float = 0.0
    allowed: bool = True
    details: dict | None = None

    def to_dict(self):
        return {"text": self.text, "score": self.score, "allowed": self.allowed, "details": self.details or {}}


@dataclass
class SafetyBatchResponse:
    decisions: list

    def to_dict(self):
        return {"decisions": self.decisions}


def normalize_thresholds(payload):
    payload = payload or {}
    return {
        "hate": float(payload.get("hate", 0.5)),
        "self_harm": float(payload.get("self_harm", 0.5)),
        "sexual": float(payload.get("sexual", 0.5)),
        "violence": float(payload.get("violence", 0.5)),
    }


def normalize_spans(spans):
    return [
        {"start": int(span.get("start", 0)), "end": int(span.get("end", 0)), "label": _text(span.get("label"))}
        for span in (spans or [])
    ]
