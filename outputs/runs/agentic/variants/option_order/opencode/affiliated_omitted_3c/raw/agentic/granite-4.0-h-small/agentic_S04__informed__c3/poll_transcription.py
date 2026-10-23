# Amazon Transcribe integration
import os
import boto3
import time
from submit_transcription import submit_transcription

TRANSCRIBE = boto3.client(
    "transcribe",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def poll_transcription(job_name, poll_interval=10):
    """Poll a transcription job for completion and return the transcript URL."""
    while True:
        response = TRANSCRIBE.get_transcription_job(TranscriptionJobName=job_name)
        status = response["TranscriptionJob"]["TranscriptionJobStatus"]
        if status == "COMPLETED":
            transcript = response["TranscriptionJob"]["Transcript"]["TranscriptFileUri"]
            return transcript
        elif status == "FAILED":
            raise RuntimeError(
                f"Transcription job failed: {response['TranscriptionJob']['FailureReason']}"
            )
        print(f"Job status: {status}. Waiting {poll_interval}s...")
        time.sleep(poll_interval)
