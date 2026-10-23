from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionJobRequest:
    audio_url: str
    webhook_url: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True


@dataclass
class TranscriptionJobResult:
    id: str
    status: str
    transcript: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    utterances: Optional[List[Dict[str, Any]]] = None
    raw: Optional[Dict[str, Any]] = None


def normalize_transcript_payload(payload: Dict[str, Any]) -> TranscriptionJobResult:
    transcript = payload.get("text") or payload.get("transcript")
    return TranscriptionJobResult(
        id=str(
            payload.get("id")
            or payload.get("job_id")
            or payload.get("request_id")
            or ""
        ),
        status=str(payload.get("status") or payload.get("state") or "unknown"),
        transcript=transcript,
        words=payload.get("words"),
        utterances=payload.get("utterances") or payload.get("segments"),
        raw=payload,
    )
