import boto3

from speech_models import normalize_segments


def timestamped_transcript(payload, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    job = response["TranscriptionJob"]
    transcript = job.get("Transcript", {})
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "segments": normalize_segments(transcript),
    }
