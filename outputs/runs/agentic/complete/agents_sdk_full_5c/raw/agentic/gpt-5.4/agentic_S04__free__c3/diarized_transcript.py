from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import get_transcript, submit_transcript_request
from speech_models import TranscriptionSubmission, normalize_segments


def diarized_transcript(
    audio_url: str,
    api_key: Optional[str] = None,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    request = TranscriptionSubmission(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=True,
    )
    payload = request.to_assemblyai_payload()
    payload["speech_model"] = "best"
    created = submit_transcript_request(payload, api_key=api_key)
    transcript = get_transcript(created["id"], api_key=api_key)
    return {
        "provider": "AssemblyAI",
        "transcript_id": created["id"],
        "status": transcript.get("status"),
        "segments": normalize_segments(transcript),
    }
