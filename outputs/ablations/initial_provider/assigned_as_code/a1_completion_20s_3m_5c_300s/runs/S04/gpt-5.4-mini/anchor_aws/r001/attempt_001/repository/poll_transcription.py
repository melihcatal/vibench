import boto3

from speech_models import normalize_transcript_result


def poll_transcription(payload, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    return normalize_transcript_result(response)
