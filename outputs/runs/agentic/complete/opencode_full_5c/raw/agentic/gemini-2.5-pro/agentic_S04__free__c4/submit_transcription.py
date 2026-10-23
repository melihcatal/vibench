from speech_client import SpeechClient
from speech_models import TranscriptionResponse


def submit_transcription_job(audio_url: str) -> TranscriptionResponse:
    """
    Submits an audio file for batch transcription using AssemblyAI.
    """
    client = SpeechClient()
    response = client.submit_transcription(audio_url)
    return response
