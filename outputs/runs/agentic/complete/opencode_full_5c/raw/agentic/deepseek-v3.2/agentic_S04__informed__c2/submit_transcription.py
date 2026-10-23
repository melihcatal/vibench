import os
import assemblyai as aai
from speech_client import get_assemblyai_client


def submit_transcription(audio_url):
    """Submit an audio file for batch transcription using AssemblyAI."""
    client = get_assemblyai_client()

    config = aai.TranscriptionConfig(
        language_code="en", speaker_labels=True, punctuate=True, format_text=True
    )

    transcript = client.transcribe.submit(audio_url=audio_url, config=config)

    return {
        "job_id": transcript.id,
        "status": transcript.status,
        "audio_url": audio_url,
        "provider": "AssemblyAI",
    }
