from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionRequest:
    audio_source: str
    webhook_url: Optional[str] = None
    language_code: Optional[str] = None
    speaker_labels: bool = False
    timestamps: bool = False


@dataclass
class TranscriptSegment:
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    speaker: Optional[str] = None


@dataclass
class TranscriptionResponse:
    id: str
    status: str
    text: str = ""
    segments: Optional[List[TranscriptSegment]] = None


def normalize_segments(raw_segments: Any) -> List[TranscriptSegment]:
    normalized: List[TranscriptSegment] = []
    for item in raw_segments or []:
        normalized.append(
            TranscriptSegment(
                text=str(item.get("text", "")),
                start=item.get("start"),
                end=item.get("end"),
                speaker=item.get("speaker"),
            )
        )
    return normalized


def response_to_dict(response: TranscriptionResponse) -> Dict[str, Any]:
    return {
        "id": response.id,
        "status": response.status,
        "text": response.text,
        "segments": [segment.__dict__ for segment in response.segments or []],
    }
