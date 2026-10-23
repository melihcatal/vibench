from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional

@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    language: Optional[str] = None


def normalize_transcript_payload(payload: Dict[str, Any]) -> TranscriptChunk:
    text = payload.get("text") or payload.get("transcript") or ""
    is_final = bool(payload.get("final") or payload.get("is_final"))
    language = payload.get("language")
    return TranscriptChunk(text=text, is_final=is_final, language=language)


def join_chunks(chunks: Iterable[TranscriptChunk]) -> str:
    return " ".join(chunk.text.strip() for chunk in chunks if chunk.text).strip()
