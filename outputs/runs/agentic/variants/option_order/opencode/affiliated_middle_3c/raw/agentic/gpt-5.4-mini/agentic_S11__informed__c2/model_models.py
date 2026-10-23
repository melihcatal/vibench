from dataclasses import dataclass


@dataclass
class PlatformRequest:
    prompt: str
    locale: str = "en"


@dataclass
class PlatformResponse:
    text: str
    model: str
    resource_id: str = ""
    usage: dict | None = None


def normalize_output(text: str) -> str:
    return " ".join(text.strip().split())
