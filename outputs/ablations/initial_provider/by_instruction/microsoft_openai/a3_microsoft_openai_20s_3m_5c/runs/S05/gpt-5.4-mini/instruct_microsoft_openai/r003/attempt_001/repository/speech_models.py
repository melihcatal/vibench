from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_language(language: Optional[str]) -> Optional[str]:
    if language is None:
        return None
    language = language.strip()
    return language or None


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    confidence: Optional[float] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def normalized(self) -> "TranscriptChunk":
        return TranscriptChunk(
            text=normalize_text(self.text),
            is_final=self.is_final,
            language=normalize_language(self.language),
            confidence=self.confidence,
            metadata=dict(self.metadata),
        )


@dataclass
class SpeechRequest:
    language: Optional[str] = None
    enable_punctuation: bool = True
    model: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


@dataclass
class SpeechResponse:
    chunks: List[TranscriptChunk] = field(default_factory=list)
    raw: Dict[str, Any] = field(default_factory=dict)


def chunks_to_text(chunks: Iterable[TranscriptChunk]) -> str:
    return "\n".join(normalize_text(chunk.text) for chunk in chunks if chunk.text)
