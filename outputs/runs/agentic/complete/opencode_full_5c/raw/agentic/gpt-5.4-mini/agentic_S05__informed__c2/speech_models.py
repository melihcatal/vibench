from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamingAudioChunk:
    data: bytes
    is_final: bool = False


@dataclass
class TranscriptResult:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None
    language: Optional[str] = None


def normalize_transcript(payload: Any) -> TranscriptResult:
    if isinstance(payload, TranscriptResult):
        return payload
    if isinstance(payload, dict):
        text = str(payload.get("text") or payload.get("transcript") or "")
        is_final = bool(
            payload.get("is_final")
            or payload.get("final")
            or payload.get("speech_final")
        )
        confidence = payload.get("confidence")
        language = payload.get("language") or payload.get("lang")
        return TranscriptResult(
            text=text, is_final=is_final, confidence=confidence, language=language
        )
    return TranscriptResult(text=str(payload), is_final=False)


def transcript_to_dict(result: TranscriptResult) -> Dict[str, Any]:
    return {
        "text": result.text,
        "is_final": result.is_final,
        "confidence": result.confidence,
        "language": result.language,
    }
