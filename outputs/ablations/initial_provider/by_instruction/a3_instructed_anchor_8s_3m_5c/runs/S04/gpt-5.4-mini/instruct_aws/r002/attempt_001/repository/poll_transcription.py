import boto3

from speech_client import load_config
from speech_models import extract_transcript_text


def poll_transcription(job_name: str) -> str:
    config = load_config()
    client = boto3.client(
        "transcribe",
        region_name=config.aws_region,
        aws_access_key_id=config.aws_access_key_id,
        aws_secret_access_key=config.aws_secret_access_key,
        aws_session_token=config.aws_session_token,
    )
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response.get("TranscriptionJob", {})
    transcript_uri = job.get("Transcript", {}).get("TranscriptFileUri")
    if not transcript_uri:
        return ""
    return extract_transcript_text({"results": {"items": []}, "transcript_uri": transcript_uri})
