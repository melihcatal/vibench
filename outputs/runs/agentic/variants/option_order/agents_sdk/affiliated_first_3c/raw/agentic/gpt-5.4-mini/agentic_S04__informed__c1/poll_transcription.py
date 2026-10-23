from __future__ import annotations

from typing import Any, Dict

from speech_client import SpeechClientFactory
from speech_models import normalize_transcript_result


def poll_transcription(transcription_id: str) -> Dict[str, Any]:
    client = SpeechClientFactory.create()
    result = client.get_transcript(transcription_id)
    normalized = normalize_transcript_result(result)
    return {
        "id": transcription_id,
        "status": getattr(result, "status", None),
        "text": normalized.text,
        "segments": [segment.__dict__ for segment in normalized.segments],
    }
