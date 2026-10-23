import boto3

from speech_client import load_config


def timestamped_transcript(job_name: str) -> dict:
    config = load_config()
    client = boto3.client(
        "transcribe",
        region_name=config.aws_region,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )
    return client.get_transcription_job(TranscriptionJobName=job_name)
