from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


def normalize_transcript(text: str) -> str:
    return " ".join(text.split()).strip()


def chunk_text(parts: Iterable[str]) -> str:
    return normalize_transcript(" ".join(part for part in parts if part))


@dataclass
class StreamingTranscriptEvent:
    text: str
    is_final: bool = False
    language_code: Optional[str] = None
    confidence: Optional[float] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StreamingTranscriptEvent":
        return cls(
            text=normalize_transcript(str(data.get("text", ""))),
            is_final=bool(data.get("is_final", False)),
            language_code=data.get("language_code"),
            confidence=data.get("confidence"),
        )


@dataclass
class CaptionChunk:
    text: str
    speaker: Optional[str] = None
    timestamp_ms: Optional[int] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": normalize_transcript(self.text),
            "speaker": self.speaker,
            "timestamp_ms": self.timestamp_ms,
        }


def caption_chunks_to_text(chunks: List[CaptionChunk]) -> str:
    return chunk_text(chunk.text for chunk in chunks)
