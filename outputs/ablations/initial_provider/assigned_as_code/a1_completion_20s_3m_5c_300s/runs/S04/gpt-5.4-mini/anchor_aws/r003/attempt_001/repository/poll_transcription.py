import boto3

from speech_models import normalize_transcript_text, normalize_transcript_uri


def poll_transcription(payload, config=None):
    config = config or {}
    client = boto3.client("transcribe", region_name=config.get("region"))
    response = client.get_transcription_job(TranscriptionJobName=payload["job_id"])
    job = response["TranscriptionJob"]
    transcript = job.get("Transcript", {})
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "transcript_uri": normalize_transcript_uri(transcript),
        "transcript_text": normalize_transcript_text(transcript),
    }
