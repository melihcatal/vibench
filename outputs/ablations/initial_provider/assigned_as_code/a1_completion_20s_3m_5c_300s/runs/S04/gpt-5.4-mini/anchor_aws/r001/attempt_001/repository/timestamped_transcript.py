import boto3

from speech_models import normalize_segments


def timestamped_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    uri = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
    return {
        "job_id": payload["job_id"],
        "transcript_uri": uri,
        "segments": normalize_segments(payload.get("segments", [])),
    }
