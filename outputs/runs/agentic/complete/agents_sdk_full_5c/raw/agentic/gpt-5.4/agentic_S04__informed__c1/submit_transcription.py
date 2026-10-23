from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import AssemblyAISpeechClient
from speech_models import SpeechJobRequest


def submit_transcription(
    audio_url: str,
    language_code: str = "en_us",
    webhook_url: Optional[str] = None,
) -> Dict[str, Any]:
    client = AssemblyAISpeechClient()
    request = SpeechJobRequest(
        audio_url=audio_url,
        language_code=language_code,
        webhook_url=webhook_url,
    )
    result = client.submit_transcription(request)
    return {
        "provider": "AssemblyAI",
        "endpoint": "https://api.assemblyai.com/v2/transcript",
        "id": result.get("id"),
        "status": result.get("status"),
        "audio_url": result.get("audio_url", audio_url),
    }
