from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import create_session, raise_for_assemblyai_error, transcript_endpoint
from speech_models import TranscriptionJobRequest, normalize_transcript_response


DEFAULT_MODEL = "best"


def submit_transcription(
    audio_url: str,
    language_code: Optional[str] = None,
    webhook_url: Optional[str] = None,
) -> Dict[str, Any]:
    session = create_session()
    request = TranscriptionJobRequest(audio_url=audio_url, language_code=language_code)
    payload = request.to_assemblyai_payload()
    payload["speech_model"] = DEFAULT_MODEL
    if webhook_url:
        payload["webhook_url"] = webhook_url

    response = session.post(transcript_endpoint(), json=payload, timeout=60)
    raise_for_assemblyai_error(response)
    normalized = normalize_transcript_response(response.json())
    return {
        "provider": "AssemblyAI",
        "transcript_id": normalized.transcript_id,
        "status": normalized.status,
    }
