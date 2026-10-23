from dataclasses import dataclass

def normalize_text(value):
    return '' if value is None else str(value).strip()

@dataclass
class PlatformRequest:
    prompt: str

@dataclass
class PlatformResult:
    text: str
    model: str
    usage: object | None = None
    raw: object | None = None
