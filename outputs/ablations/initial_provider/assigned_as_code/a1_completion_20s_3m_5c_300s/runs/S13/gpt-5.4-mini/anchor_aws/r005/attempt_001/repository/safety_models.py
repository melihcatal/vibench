from dataclasses import dataclass


def _text(value):
    return "" if value is None else str(value)


@dataclass
class TextModerationRequest:
    text: str

    @classmethod
    def from_payload(cls, payload):
        return cls(text=_text((payload or {}).get("text")))


@dataclass
class BatchModerationRequest:
    texts: list

    @classmethod
    def from_payload(cls, payload):
        items = (payload or {}).get("texts") or []
        return cls(texts=[_text(item) for item in items])


def normalize_categories(categories):
    result = {}
    for item in categories or []:
        name = item.get("Name") or item.get("category") or item.get("name")
        score = item.get("Score") if "Score" in item else item.get("score")
        if name is not None:
            result[str(name)] = float(score or 0.0)
    return result


def build_decision(allow, categories, reason=None):
    decision = {"allow": bool(allow), "categories": categories}
    if reason is not None:
        decision["reason"] = reason
    return decision
