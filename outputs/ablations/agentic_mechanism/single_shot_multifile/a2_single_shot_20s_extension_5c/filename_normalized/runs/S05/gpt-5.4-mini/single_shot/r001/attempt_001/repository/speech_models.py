from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class StreamingTranscriptEvent:
    transcript: str
    is_final: bool
    confidence: Optional[float]
    language_code: str


def normalize_stream_event(transcript: str, is_final: bool, confidence: Any = None, language_code: str = 'en-US') -> Dict[str, object]:
    conf = None
    try:
        if confidence is not None:
            conf = float(confidence)
    except (TypeError, ValueError):
        conf = None
    return {
        'transcript': transcript.strip(),
        'is_final': bool(is_final),
        'confidence': conf,
        'language_code': language_code,
    }

