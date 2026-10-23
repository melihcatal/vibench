from dataclasses import dataclass
from typing import Iterable, List, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    language_code: Optional[str] = None


def normalize_text(text: str) -> str:
    return " ".join(text.strip().split())


def join_chunks(chunks: Iterable[TranscriptChunk]) -> str:
    parts: List[str] = []
    for chunk in chunks:
        cleaned = normalize_text(chunk.text)
        if cleaned:
            parts.append(cleaned)
    return " ".join(parts)


def best_transcript(texts: Iterable[str]) -> str:
    for text in texts:
        cleaned = normalize_text(text)
        if cleaned:
            return cleaned
    return ""
