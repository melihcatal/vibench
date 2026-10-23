from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import AssemblyAIBatchSpeechClient
from speech_models import BatchTranscriptionRequest


def submit_transcription(
    audio_url: str,
    language_code: Optional[str] = None,
    webhook_url: Optional[str] = None,
) -> Dict[str, Any]:
    client = AssemblyAIBatchSpeechClient()
    request = BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        webhook_url=webhook_url,
    )
    job = client.submit_transcription(request)
    return {
        "provider": "AssemblyAI",
        "api_base": "https://api.assemblyai.com/v2",
        "transcript_id": job.transcript_id,
        "status": job.status,
    }
