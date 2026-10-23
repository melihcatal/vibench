from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import get_speech_client
from speech_models import TranscriptionJobRequest, normalize_transcript_response



def submit_transcription(audio_url: str, language_code: Optional[str] = None) -> Dict[str, Any]:
    client = get_speech_client()
    request = TranscriptionJobRequest(audio_url=audio_url, language_code=language_code)
    data = client.post("transcript", request.to_assemblyai_payload())
    result = normalize_transcript_response(data)
    return {
        "provider": "AssemblyAI",
        "api_base": "https://api.assemblyai.com/v2",
        "transcript_id": result.transcript_id,
        "status": result.status,
        "raw": data,
    }
