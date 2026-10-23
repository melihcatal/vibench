from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptRequest:
    audio_url: str
    language_code: Optional[str] = None
    diarization: bool = False
    punctuate: bool = True
    format_text: bool = True
    word_boost: List[str] = field(default_factory=list)


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    speaker: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None


@dataclass
class TranscriptResponse:
    transcript_id: str
    status: str
    text: str
    segments: List[TranscriptSegment] = field(default_factory=list)


def normalize_transcript_result(result: Any) -> TranscriptResponse:
    segments: List[TranscriptSegment] = []
    for item in getattr(result, "utterances", []) or []:
        segments.append(
            TranscriptSegment(
                text=getattr(item, "text", ""),
                start=getattr(item, "start", None),
                end=getattr(item, "end", None),
                speaker=str(getattr(item, "speaker", None)) if getattr(item, "speaker", None) is not None else None,
                words=getattr(item, "words", None),
            )
        )
    return TranscriptResponse(
        transcript_id=str(getattr(result, "id", "")),
        status=str(getattr(result, "status", "")),
        text=str(getattr(result, "text", "")),
        segments=segments,
    )
