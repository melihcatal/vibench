from dataclasses import dataclass
from typing import Any, Dict, List, Optional

@dataclass
class TranscriptRequest:
    audio_url: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    word_boost: Optional[List[str]] = None


def normalize_transcript_payload(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": payload.get("id") or payload.get("job_id"),
        "status": payload.get("status"),
        "text": payload.get("text") or payload.get("transcript") or "",
        "words": payload.get("words") or [],
        "utterances": payload.get("utterances") or [],
        "segments": payload.get("segments") or [],
        "summary": payload.get("summary") or "",
    }
