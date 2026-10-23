from typing import Any, Dict

from speech_client import get_client
from speech_models import normalize_transcription_response


def poll_transcription(transcription_id: str) -> Dict[str, Any]:
    client = get_client()
    response = client.audio.transcriptions.retrieve(transcription_id)
    normalized = normalize_transcription_response(response)
    return {"job_id": normalized.job_id, "text": normalized.text, "raw": normalized.raw}
