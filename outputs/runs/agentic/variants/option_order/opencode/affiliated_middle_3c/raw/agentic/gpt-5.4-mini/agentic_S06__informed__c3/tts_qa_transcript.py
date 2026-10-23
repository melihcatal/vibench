import os

import boto3


def transcribe_audio_job(bucket: str, key: str, language_code: str = "en-US") -> dict:
    client = boto3.client("transcribe")
    job_name = key.replace("/", "-")
    media_uri = f"s3://{bucket}/{key}"
    client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={"MediaFileUri": media_uri},
        MediaFormat="mp3",
        LanguageCode=language_code,
    )
    return client.get_transcription_job(TranscriptionJobName=job_name)
