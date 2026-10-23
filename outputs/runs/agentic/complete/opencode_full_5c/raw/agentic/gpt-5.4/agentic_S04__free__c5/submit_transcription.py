from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import AssemblyAIClient
from speech_models import TranscriptionSubmission, normalize_transcript_response


def submit_transcription(
    audio_url: str,
    language_code: Optional[str] = None,
    webhook_url: Optional[str] = None,
    word_boost: Optional[List[str]] = None,
) -> Dict[str, Any]:
    client = AssemblyAIClient()
    request = TranscriptionSubmission(
        audio_url=audio_url,
        language_code=language_code,
        webhook_url=webhook_url,
        word_boost=word_boost or [],
    )
    payload = client.submit_transcript(request.to_assemblyai_payload())
    transcript = normalize_transcript_response(payload)
    return {"id": transcript.id, "status": transcript.status, "provider": "assemblyai"}
