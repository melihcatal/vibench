from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import AssemblyAIClient, build_transcription_request


def submit_audio_for_batch_transcription(
    audio_url: str,
    language_code: Optional[str] = None,
    webhook_url: Optional[str] = None,
) -> Dict[str, Any]:
    client = AssemblyAIClient()
    request = build_transcription_request(
        audio_url=audio_url,
        language_code=language_code,
        webhook_url=webhook_url,
    )
    result = client.submit_transcription(request)
    return {
        "provider": "AssemblyAI",
        "api_base": "https://api.assemblyai.com/v2",
        "speech_model": "best",
        "transcript_id": result.transcript_id,
        "status": result.status,
    }
