from google.cloud import speech_v2 as speech
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import SpeechNormalizer, TranscriptionResult
import os


def poll_transcription(job_path: str) -> TranscriptionResult:
    config = TranscriptionConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        recognizer_id=os.getenv("GOOGLE_CLOUD_RECOGNIZER_ID"),
    )

    client = SpeechClient(config)
    response = client.poll_transcription_job(job_path)
    return SpeechNormalizer.normalize_response(response)
