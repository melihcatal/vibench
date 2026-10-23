from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class TranslationRequest:
    text: str
    source_language: str | None
    target_language: str


@dataclass(frozen=True)
class TranslationResponse:
    translated_text: str
    source_language: str | None
    target_language: str


def normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value)


def serialize_response(response: TranslationResponse) -> dict[str, Any]:
    return asdict(response)
