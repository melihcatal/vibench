from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_partial: bool = False
    language_code: Optional[str] = None


def normalize_transcript_text(text: str) -> str:
    return " ".join(text.split()).strip()


def chunk_to_dict(chunk: TranscriptChunk) -> Dict[str, Any]:
    return {
        "text": normalize_transcript_text(chunk.text),
        "is_partial": chunk.is_partial,
        "language_code": chunk.language_code,
    }


def collect_text(chunks: Iterable[TranscriptChunk]) -> str:
    return "\n".join(normalize_transcript_text(chunk.text) for chunk in chunks if chunk.text)
