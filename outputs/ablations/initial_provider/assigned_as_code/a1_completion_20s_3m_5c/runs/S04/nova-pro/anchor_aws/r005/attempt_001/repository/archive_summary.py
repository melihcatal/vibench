import boto3

from speech_client import get_speech_client


def archive_summary(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    transcript = job["Transcript"]
    items = transcript.get("Items", [])
    summary = ' '.join([item["alternatives"][0]["transcript"] for item in items])
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "summary": summary
    }