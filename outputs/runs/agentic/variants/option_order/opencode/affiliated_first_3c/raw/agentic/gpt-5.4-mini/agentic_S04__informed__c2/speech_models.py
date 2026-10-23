from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionSubmitRequest:
    audio_url: str
    language: str = "en-US"
    display_name: Optional[str] = None


@dataclass
class TranscriptWord:
    word: str
    start: float
    end: float
    speaker: Optional[str] = None


@dataclass
class TranscriptSegment:
    text: str
    start: float = 0.0
    duration: float = 0.0
    speaker: Optional[str] = None
    words: List[TranscriptWord] = field(default_factory=list)


def build_transcript_payload(raw: Dict[str, Any]) -> Dict[str, Any]:
    segments = raw.get("segments", raw.get("utterances", []))
    return {
        "status": raw.get("status", ""),
        "transcript": raw.get("transcript", raw.get("text", "")),
        "segments": [
            {
                "text": s.get("text", ""),
                "start": s.get("start", s.get("offset", 0)),
                "duration": s.get("duration", 0),
                "speaker": s.get("speaker", s.get("speaker_label")),
                "words": s.get("words", []),
            }
            for s in segments
        ],
    }
