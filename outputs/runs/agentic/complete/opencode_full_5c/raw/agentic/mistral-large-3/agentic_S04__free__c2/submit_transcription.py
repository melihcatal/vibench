from google.cloud import speech_v2 as speech
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import SpeechNormalizer
import os


def submit_transcription(audio_uri: str, job_name: str) -> str:
    config = TranscriptionConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        recognizer_id=os.getenv("GOOGLE_CLOUD_RECOGNIZER_ID"),
    )

    client = SpeechClient(config)
    job_path = client.submit_transcription_job(audio_uri, job_name)
    return job_path
