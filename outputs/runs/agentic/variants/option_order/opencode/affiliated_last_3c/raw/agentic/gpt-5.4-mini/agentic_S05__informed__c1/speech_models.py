from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    language: Optional[str] = None
    alternatives: Optional[List[str]] = None


def normalize_transcript(payload: Any) -> TranscriptChunk:
    if isinstance(payload, TranscriptChunk):
        return payload
    text = ""
    is_final = False
    language = None
    alternatives = None
    if isinstance(payload, dict):
        text = str(payload.get("text") or payload.get("transcript") or "")
        is_final = bool(payload.get("is_final", payload.get("final", False)))
        language = payload.get("language") or payload.get("locale")
        alts = payload.get("alternatives")
        if isinstance(alts, list):
            alternatives = [str(item) for item in alts]
    else:
        text = str(payload)
    return TranscriptChunk(
        text=text, is_final=is_final, language=language, alternatives=alternatives
    )


def chunk_texts(chunks: Iterable[Any]) -> List[str]:
    return [normalize_transcript(chunk).text for chunk in chunks]
