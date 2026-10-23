from dataclasses import dataclass


def normalize_text(value):
    return "" if value is None else str(value).strip()


def normalize_text_list(values):
    return [normalize_text(value) for value in (values or [])]


@dataclass
class SafetyConfig:
    endpoint: str
    api_key: str


@dataclass
class ModerationDecision:
    text: str
    toxicity: float
    allow: bool
