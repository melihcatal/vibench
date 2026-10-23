import json
from dataclasses import dataclass
from typing import Any


@dataclass
class ChatGenerationRequest:
    system_prompt: str
    user_prompt: str
    max_output_tokens: int
    temperature: float = 0.0


@dataclass
class TextResult:
    provider: str
    model: str
    text: str


@dataclass
class JsonResult:
    provider: str
    model: str
    data: dict[str, Any]


@dataclass
class AnswerResult:
    provider: str
    model: str
    answer: str
    context_used: bool


@dataclass
class SafetyResult:
    provider: str
    model: str
    flagged: bool
    categories: dict[str, bool]


@dataclass
class EmbeddingResult:
    provider: str
    model: str
    embedding: list[float]


@dataclass
class AudioResult:
    provider: str
    model: str
    audio_bytes: bytes
    transcript: str


def normalize_text(value: str) -> str:
    return value.strip()


def parse_json_text(value: str) -> dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Expected top-level JSON object")
    return parsed


def normalize_categories(categories: Any) -> dict[str, bool]:
    if hasattr(categories, "model_dump"):
        raw = categories.model_dump()
    elif isinstance(categories, dict):
        raw = categories
    else:
        raw = vars(categories)
    return {str(key): bool(value) for key, value in raw.items()}
