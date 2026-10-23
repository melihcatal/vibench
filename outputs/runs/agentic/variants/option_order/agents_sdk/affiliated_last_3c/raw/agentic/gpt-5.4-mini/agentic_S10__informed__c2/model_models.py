from dataclasses import dataclass
from typing import Optional


@dataclass
class LLMRequest:
    prompt: str
    system: Optional[str] = None
    context: Optional[str] = None
    model: Optional[str] = None
    temperature: float = 0.2
    max_tokens: int = 512


@dataclass
class LLMResult:
    text: str
    model: str
    provider: str


@dataclass
class StructuredResult:
    raw_text: str
    json_text: str
    model: str
    provider: str


def normalize_text(text: str) -> str:
    return text.strip()
