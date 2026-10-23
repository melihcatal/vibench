import boto3

from speech_client import get_speech_client


def timestamped_transcript(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    transcript = job["Transcript"]
    timestamps = transcript.get("Items", [])
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "timestamps": timestamps
    }