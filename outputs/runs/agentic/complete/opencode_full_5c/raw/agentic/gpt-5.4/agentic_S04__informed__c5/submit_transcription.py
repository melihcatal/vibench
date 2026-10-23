from __future__ import annotations

from typing import Any, Dict

from speech_client import assemblyai_post, build_batch_transcription_payload
from speech_models import TranscriptionJobRequest


def submit_transcription(
    audio_url: str, language_code: str = "en_us"
) -> Dict[str, Any]:
    request = TranscriptionJobRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=False,
        word_timestamps=True,
    )
    payload = build_batch_transcription_payload(request)
    result = assemblyai_post("/transcript", payload)
    return {
        "provider": "AssemblyAI",
        "provider_api": "https://api.assemblyai.com/v2/transcript",
        "transcript_id": result["id"],
        "status": result.get("status", "queued"),
    }
