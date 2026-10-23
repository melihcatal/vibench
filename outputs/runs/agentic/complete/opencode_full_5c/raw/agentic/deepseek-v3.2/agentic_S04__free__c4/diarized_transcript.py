import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import (
    RecognitionAudio,
    RecognitionConfig,
    SpeakerDiarizationConfig,
)
from speech_client import get_speech_client


def diarized_transcript(
    audio_file_path, language_code="en-US", min_speaker_count=2, max_speaker_count=5
):
    """Request speaker diarization for a recorded meeting using Google Cloud Speech-to-Text."""
    client = get_speech_client()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = RecognitionAudio(content=content)

    diarization_config = SpeakerDiarizationConfig(
        enable_speaker_diarization=True,
        min_speaker_count=min_speaker_count,
        max_speaker_count=max_speaker_count,
    )

    config = RecognitionConfig(
        encoding=speech_v1.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        diarization_config=diarization_config,
        enable_word_time_offsets=True,
    )

    operation = client.long_running_recognize(config=config, audio=audio)
    return operation.name
