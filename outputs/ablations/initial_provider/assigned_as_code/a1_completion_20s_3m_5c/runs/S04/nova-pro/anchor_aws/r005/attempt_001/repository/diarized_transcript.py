import boto3

from speech_client import get_speech_client


def diarized_transcript(job_id, config=None):
    client = get_speech_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    transcript = job["Transcript"]
    diarization = transcript.get("SpeakerLabels", {})
    return {
        "job_id": job["TranscriptionJobName"],
        "status": job["TranscriptionJobStatus"],
        "diarization": diarization
    }