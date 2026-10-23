import os
import boto3
from speech_client import get_transcribe_client

def poll_transcription(job_name):
    # Use Amazon Transcribe as the concrete provider
    client = get_transcribe_client()
    # Poll the status of the batch transcription job
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job_status = response['TranscriptionJob']['TranscriptionJobStatus']
    print(f"Job status: {job_status}")
    if job_status == 'COMPLETED':
        transcript_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
        print(f"Transcript ready at: {transcript_uri}")
        return transcript_uri
    elif job_status == 'FAILED':
        error = response['TranscriptionJob']['FailureReason']
        print(f"Job failed: {error}")
        return None
    else:
        return None  # Job still in progress