import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio


def submit_transcription(audio_file_path, language_code="en-US"):
    """Submit an audio file for batch transcription using Google Cloud Speech-to-Text."""
    client = speech_v1.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = RecognitionAudio(content=content)

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_word_time_offsets=True,
        model="video",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print(f"Submitted transcription job: {operation.operation.name}")
    return operation.operation.name
