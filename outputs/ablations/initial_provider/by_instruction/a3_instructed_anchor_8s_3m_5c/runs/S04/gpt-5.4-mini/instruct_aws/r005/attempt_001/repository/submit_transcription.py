import boto3

from speech_client import load_config, s3_uri_from_path
from speech_models import TranscriptionRequest


def submit_transcription(audio_path: str, job_name: str | None = None) -> dict:
    config = load_config()
    client = boto3.client("transcribe", region_name=config.region)
    audio_uri = s3_uri_from_path(audio_path)
    request = TranscriptionRequest(audio_uri=audio_uri, job_name=job_name or "batch-transcription", language_code=config.language_code)
    response = client.start_transcription_job(
        TranscriptionJobName=request.job_name,
        Media={"MediaFileUri": request.audio_uri},
        MediaFormat=request.media_format,
        LanguageCode=request.language_code,
    )
    return response
