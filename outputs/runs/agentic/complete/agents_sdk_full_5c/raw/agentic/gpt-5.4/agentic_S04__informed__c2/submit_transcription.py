from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import build_speech_client
from speech_models import TranscriptionSubmission


def submit_transcription(
    audio_path: Optional[str] = None,
    audio_url: Optional[str] = None,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    client = build_speech_client()
    resolved_audio_url = audio_url or (client.upload_audio(audio_path) if audio_path else None)
    if not resolved_audio_url:
        raise ValueError("audio_path or audio_url is required")

    request = TranscriptionSubmission(
        audio_url=resolved_audio_url,
        audio_path=audio_path,
        language_code=language_code,
    )
    job = client.submit_transcript(request.to_assemblyai_payload())
    return {
        "provider": "AssemblyAI",
        "transcript_id": job["id"],
        "status": job.get("status"),
        "audio_url": resolved_audio_url,
    }
