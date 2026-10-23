import os
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import TranscriptionRequest


def submit_transcription(audio_url: str) -> str:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    Returns the transcription job ID.
    """
    client = SpeechClient()
    config = TranscriptionConfig(audio_url=audio_url)
    result = client.submit_transcription(config)
    return result.id
