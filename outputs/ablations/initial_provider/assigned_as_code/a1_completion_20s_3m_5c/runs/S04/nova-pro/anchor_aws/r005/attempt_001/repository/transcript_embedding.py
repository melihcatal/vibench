import boto3

from speech_client import get_speech_client


def transcript_embedding(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    transcript = job["Transcript"]
    items = transcript.get("Items", [])
    embeddings = []
    for item in items:
        text = item["alternatives"][0]["transcript"]
        embeddings.append({
            "start_time": item["start_time"],
            "end_time": item["end_time"],
            "text": text,
            "embedding": None  # Placeholder for actual embedding
        })
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "embeddings": embeddings
    }