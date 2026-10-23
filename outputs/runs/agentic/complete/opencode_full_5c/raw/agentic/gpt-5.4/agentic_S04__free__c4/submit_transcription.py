from __future__ import annotations

from speech_client import AssemblyAISpeechClient
from speech_models import TranscriptionJobRequest


def submit_transcription(
    audio_url: str, language_code: str = "en_us"
) -> dict[str, str]:
    client = AssemblyAISpeechClient()
    job = client.submit_transcription(
        TranscriptionJobRequest(
            audio_url=audio_url,
            language_code=language_code,
            speaker_labels=False,
        )
    )
    return {
        "provider": "AssemblyAI",
        "transcript_id": job["id"],
        "status": job.get("status", "queued"),
    }
