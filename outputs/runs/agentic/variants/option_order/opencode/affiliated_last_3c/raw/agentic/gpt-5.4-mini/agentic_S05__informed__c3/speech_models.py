import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_language(language: Optional[str]) -> Optional[str]:
    if language is None:
        return None
    value = language.strip()
    return value or None


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    language: Optional[str] = None

    @classmethod
    def from_payload(cls, payload: Dict[str, Any]) -> "TranscriptEvent":
        return cls(
            text=normalize_text(str(payload.get("text", ""))),
            is_final=bool(payload.get("is_final", False)),
            language=normalize_language(payload.get("language")),
        )


def coerce_chunks(chunks: Iterable[bytes]) -> List[bytes]:
    return [chunk for chunk in chunks if chunk]
