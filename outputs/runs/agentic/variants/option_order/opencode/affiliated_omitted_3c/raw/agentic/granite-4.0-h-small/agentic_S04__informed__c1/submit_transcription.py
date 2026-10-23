import os
from speech_client import BatchSpeechClient


def submit_transcription(audio_path: str, language: str = "en-US") -> str:
    """Submit an audio file for batch transcription.

    Returns the job ID for later polling.
    """
    client = BatchSpeechClient()
    # Use AssemblyAI as the concrete provider
    response = client.transcribe(
        audio_path=audio_path,
        model="assemblyai/speech-to-text-model",
        language=language,
    )
    return response.job_id
