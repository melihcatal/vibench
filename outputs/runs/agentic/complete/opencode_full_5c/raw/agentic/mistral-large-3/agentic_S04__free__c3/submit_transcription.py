from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import SpeechClient
from speech_models import TranscriptionConfig
import os


def submit_transcription(audio_uri: str) -> str:
    """Submit an audio file for batch transcription using Google Cloud Speech-to-Text."""
    diarization_config = types.SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=2,
        max_speaker_count=10,
    )
    config = TranscriptionConfig(
        language_code="en-US",
        model="latest_long",
        use_enhanced=True,
        diarization_config=diarization_config,
        enable_word_time_offsets=True,
    )
    client = SpeechClient(config)
    operation_name = client.submit_transcription(audio_uri)
    return operation_name
