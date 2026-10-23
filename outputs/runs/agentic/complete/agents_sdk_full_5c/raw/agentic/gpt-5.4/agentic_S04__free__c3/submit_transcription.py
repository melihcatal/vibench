from __future__ import annotations

from typing import Any, Dict, List, Optional

from speech_client import submit_transcript_request
from speech_models import TranscriptionSubmission


def submit_transcription(
    audio_url: str,
    language_code: Optional[str] = None,
    word_boost: Optional[List[str]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    request = TranscriptionSubmission(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=False,
        word_boost=word_boost or [],
    )
    payload = request.to_assemblyai_payload()
    payload["punctuate"] = True
    payload["format_text"] = True
    payload["speech_model"] = "best"
    response = submit_transcript_request(payload, api_key=api_key)
    return {
        "provider": "AssemblyAI",
        "endpoint": "https://api.assemblyai.com/v2/transcript",
        "transcript_id": response["id"],
        "status": response.get("status", "queued"),
    }
