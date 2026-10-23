import os
from speech_client import get_assemblyai_client
from speech_models import TranscriptionRequest

def submit_transcription(audio_url: str) -> str:
    client = get_assemblyai_client()
    request = TranscriptionRequest(audio_url=audio_url)
    transcript = client.transcripts.submit(
        audio_url=request.audio_url,
        speaker_labels=True,
        word_timestamps=True
    )
    return transcript.id