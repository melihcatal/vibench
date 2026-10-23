import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import RecognitionConfig, RecognitionAudio


def submit_batch_transcription(audio_file_path, language_code="en-US"):
    """Submit an audio file for batch transcription using Google Cloud Speech-to-Text API."""
    client = speech_v1.SpeechClient()

    with open(audio_file_path, "rb") as audio_file:
        content = audio_file.read()

    audio = RecognitionAudio(content=content)

    config = RecognitionConfig(
        encoding=RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code=language_code,
        enable_automatic_punctuation=True,
        model="default",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    return operation.name


if __name__ == "__main__":
    job_id = submit_batch_transcription("sample_audio.wav")
    print(f"Submitted transcription job: {job_id}")
