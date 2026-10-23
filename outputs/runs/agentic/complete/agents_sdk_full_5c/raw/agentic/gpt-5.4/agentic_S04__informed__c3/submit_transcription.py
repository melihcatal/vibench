from __future__ import annotations

from typing import Optional

from speech_client import AssemblyAIClient, build_batch_request


def submit_transcription(
    audio_url: str,
    language_code: Optional[str] = None,
    webhook_url: Optional[str] = None,
) -> dict:
    client = AssemblyAIClient()
    request = build_batch_request(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=False,
        webhook_url=webhook_url,
    )
    result = client.submit_transcription(request)
    return {
        "provider": "AssemblyAI",
        "api_base": client.api_base,
        "transcript_id": result.transcript_id,
        "status": result.status,
    }
