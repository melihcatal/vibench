from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPICallError, RetryError
from speech_client import SpeechClient
from speech_models import SpeechNormalizer, TranscriptionResult
import time


def submit_transcription(audio_file_path: str) -> str:
    """
    Submits an audio file for batch transcription using Google Cloud Speech-to-Text.

    Args:
        audio_file_path: Google Cloud Storage URI (gs://) of the audio file.

    Returns:
        Operation name (str) for polling the transcription status.
    """
    client = SpeechClient()
    operation_name = client.submit_transcription(audio_file_path)
    return operation_name
