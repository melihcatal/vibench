from dataclasses import dataclass


@dataclass
class PlatformRequest:
    prompt: str
    resource_id: str | None = None
    locale: str = "en"


@dataclass
class PlatformResponse:
    text: str
    resource_id: str | None = None
    model: str | None = None
    usage: dict | None = None


def normalize_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    if hasattr(value, "output_text"):
        return str(value.output_text).strip()
    return str(value).strip()
