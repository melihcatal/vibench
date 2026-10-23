from typing import Any, Dict

import assemblyai as aai

from speech_client import configure_client
from speech_models import normalize_transcript_result


def poll_transcription(transcript_id: str) -> Dict[str, Any]:
    client = configure_client()
    transcript = client.get_by_id(transcript_id)
    normalized = normalize_transcript_result(transcript)
    return {
        "transcript_id": normalized.transcript_id,
        "status": normalized.status,
        "text": normalized.text,
        "segments": [segment.__dict__ for segment in normalized.segments],
    }
