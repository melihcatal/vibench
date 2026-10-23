from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import SpeechModels
import os


def submit_transcription(audio_file_path: str) -> str:
    """Submit an audio file for batch transcription using Google Cloud Speech-to-Text."""
    client_helper = SpeechClient()
    client = client_helper.get_client()

    audio = client_helper.load_audio(audio_file_path)
    config = client_helper.create_recognition_config()

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.name
