from dataclasses import dataclass


@dataclass
class PlatformRequest:
    prompt: str
    temperature: float = 0.2


@dataclass
class PlatformResponse:
    text: str
    model: str | None = None
    usage: dict | None = None
    resource_id: str | None = None


def normalize_text(value) -> str:
    return "" if value is None else str(value).strip()
