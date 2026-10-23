from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client, get_audio_config, SpeechConfig
from speech_models import TranscriptionResult, normalize_response
import os


def submit_transcription(audio_uri: str, config: SpeechConfig) -> str:
    """Submit an audio file to Google Cloud Speech-to-Text for batch transcription."""
    client = get_speech_client()
    audio_config = get_audio_config(config, audio_uri)
    recognition_audio = types.RecognitionAudio(uri=audio_uri)

    operation = client.long_running_recognize(
        config=audio_config,
        audio=recognition_audio,
    )

    return operation.name
