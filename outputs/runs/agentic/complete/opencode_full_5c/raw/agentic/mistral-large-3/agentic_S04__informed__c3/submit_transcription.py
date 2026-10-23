import os
import time
from typing import Optional
from speech_client import SpeechClient
from speech_models import TranscriptionJobRequest, TranscriptionJobResponse


def submit_transcription(
    audio_uri: str, job_name: str, language_code: str = "en-US"
) -> TranscriptionJobResponse:
    client = SpeechClient()
    request = TranscriptionJobRequest(
        job_name=job_name,
        media_uri=audio_uri,
        language_code=language_code,
        media_format=audio_uri.split(".")[-1],
        output_bucket=os.getenv("AWS_TRANSCRIBE_OUTPUT_BUCKET"),
    )
    return client.submit_transcription_job(request)
