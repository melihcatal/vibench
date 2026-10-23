import boto3

from speech_client import get_transcribe_client


def timestamped_transcript(job_id, config=None):
    client = get_transcribe_client(config)
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    job = response["TranscriptionJob"]
    if job["TranscriptionJobStatus"]!= "COMPLETED":
        raise ValueError("Transcription job is not completed")
    transcript_uri = job["Transcript"]["TranscriptFileUri"]
    response = client.get_transcription_job(TranscriptionJobName=job_id)
    transcript = response["TranscriptionJob"]["Transcript"]
    return transcript["Results"]
