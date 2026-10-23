from __future__ import annotations

from typing import Any, Dict, Optional

from speech_client import build_transcriber, build_transcription_config
from speech_models import TranscriptionSubmission, normalize_assemblyai_transcript


def submit_transcription(
    audio_url: str,
    language_code: Optional[str] = None,
) -> Dict[str, Any]:
    request = TranscriptionSubmission(audio_url=audio_url, language_code=language_code)
    transcriber = build_transcriber()
    config = build_transcription_config(language_code=request.language_code)
    transcript = transcriber.submit(request.audio_url, config=config)
    normalized = normalize_assemblyai_transcript(transcript)
    return {
        "provider": "AssemblyAI",
        "job_id": normalized.job_id,
        "status": normalized.status,
        "audio_url": normalized.audio_url or audio_url,
    }
