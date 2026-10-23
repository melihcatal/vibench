from __future__ import annotations

import os
from typing import Any, Dict

import boto3


TRANSCRIBE_REGION = os.getenv("AWS_DEFAULT_REGION", os.getenv("AWS_REGION", "us-east-1"))


def transcribe_qa_sample(media_uri: str, media_format: str = "mp3", language_code: str = "en-US") -> Dict[str, Any]:
    client = boto3.client("transcribe", region_name=TRANSCRIBE_REGION)
    job_name = "tts-qa-transcript-job"
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": media_uri},
        MediaFormat=media_format,
        LanguageCode=language_code,
        OutputBucketName=os.getenv("TRANSCRIBE_OUTPUT_BUCKET"),
    )
    return client.get_transcription_job(TranscriptionJobName=job_name)
