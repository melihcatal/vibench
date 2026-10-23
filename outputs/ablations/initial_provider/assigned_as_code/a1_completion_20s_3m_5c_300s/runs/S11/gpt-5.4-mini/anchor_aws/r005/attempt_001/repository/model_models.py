from dataclasses import dataclass


@dataclass
class PlatformRequest:
    text: str


@dataclass
class PlatformResponse:
    text: str
    metadata: dict


def normalize_text(value):
    if value is None:
        return ""
    if isinstance(value, str):
        return value.strip()
    return str(value).strip()
