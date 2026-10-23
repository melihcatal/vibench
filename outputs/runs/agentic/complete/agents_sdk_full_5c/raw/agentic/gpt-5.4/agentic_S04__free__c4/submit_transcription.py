from __future__ import annotations

from speech_client import assemblyai_post
from speech_models import BatchTranscriptionRequest, normalize_assemblyai_transcript


def submit_transcription(audio_url: str, language_code: str | None = None) -> dict:
    request = BatchTranscriptionRequest(
        audio_url=audio_url,
        language_code=language_code,
        speaker_labels=False,
        punctuate=True,
        format_text=True,
    )
    payload = request.to_assemblyai_payload()
    response = assemblyai_post("/transcript", payload)
    transcript = normalize_assemblyai_transcript(response)
    return {
        "provider": "AssemblyAI",
        "transcript_id": transcript.transcript_id,
        "status": transcript.status,
    }
