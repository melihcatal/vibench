from google.cloud import speech_v2 as speech
from speech_client import SpeechClient, TranscriptionConfig
from speech_models import SpeechNormalizer, DiarizationResult
import os


def request_diarization(job_path: str, speaker_count: int) -> DiarizationResult:
    config = TranscriptionConfig(
        project_id=os.getenv("GOOGLE_CLOUD_PROJECT_ID"),
        location=os.getenv("GOOGLE_CLOUD_LOCATION", "us-central1"),
        recognizer_id=os.getenv("GOOGLE_CLOUD_RECOGNIZER_ID"),
    )

    client = SpeechClient(config)
    client.enable_diarization(job_path, speaker_count)
    response = client.poll_transcription_job(job_path)
    return SpeechNormalizer.normalize_diarization(response)
