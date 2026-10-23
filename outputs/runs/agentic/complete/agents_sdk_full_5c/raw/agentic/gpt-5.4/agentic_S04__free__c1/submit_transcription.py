from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import submit_assemblyai_transcript
from speech_models import normalize_assemblyai_transcript


def submit_transcription(
    audio_url: str,
    *,
    api_key: Optional[str] = None,
    language_code: Optional[str] = None,
    speech_model: str = "best",
) -> Dict[str, Any]:
    payload = submit_assemblyai_transcript(
        audio_url,
        api_key=api_key,
        language_code=language_code,
        speech_model=speech_model,
        speaker_labels=False,
    )
    job = normalize_assemblyai_transcript(payload)
    return {
        "provider": "assemblyai",
        "job_id": job.job_id,
        "status": job.status,
        "audio_url": job.audio_url,
        "speech_model": speech_model,
    }
