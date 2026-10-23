from google.cloud import speech_v2 as speech
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import SpeechNormalizer, TranscriptionResult
import os


def get_timestamped_transcript(job_path: str) -> TranscriptionResult:
    config = TranscriptionConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        recognizer_id=os.getenv("GOOGLE_CLOUD_RECOGNIZER_ID"),
    )

    client = SpeechClient(config)
    response = client.get_transcript_with_timestamps(job_path)
    return SpeechNormalizer.normalize_response(response)
