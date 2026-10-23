from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class AudioChunk:
    data: bytes
    timestamp_ms: int = 0


@dataclass
class TranscriptEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    language_code: Optional[str] = None


def normalize_transcript_event(payload: Dict[str, Any]) -> TranscriptEvent:
    text = payload.get("Transcript", {}).get("Results", [{}])[0].get("Alternatives", [{}])[0].get("Transcript", "")
    is_final = not payload.get("Transcript", {}).get("Results", [{}])[0].get("IsPartial", True)
    confidence = payload.get("Transcript", {}).get("Results", [{}])[0].get("Alternatives", [{}])[0].get("Confidence")
    language_code = payload.get("LanguageCode") or payload.get("Transcript", {}).get("LanguageCode")
    return TranscriptEvent(text=text, is_final=is_final, confidence=confidence, language_code=language_code)
