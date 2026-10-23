import json
from dataclasses import dataclass


@dataclass
class PlatformRequest:
    prompt: str
    temperature: float = 0.2
    max_tokens: int = 256


@dataclass
class PlatformResponse:
    text: str
    model_id: str | None = None
    usage: dict | None = None
    raw: object | None = None


def normalize_text(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "".join(normalize_text(item) for item in value)
    if isinstance(value, dict):
        for key in ("text", "content", "outputText", "generated_text"):
            if key in value:
                return normalize_text(value[key])
    return json.dumps(value, default=str)
