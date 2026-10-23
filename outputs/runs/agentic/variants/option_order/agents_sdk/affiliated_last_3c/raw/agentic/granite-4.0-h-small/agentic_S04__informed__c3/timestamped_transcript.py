import os
import boto3
from speech_client import get_transcribe_client

def timestamped_transcript(job_name):
    client = get_transcribe_client()
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    transcript = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
    # Assuming the standard JSON format with 'items' containing timestamps
    print(f"Timestamped transcript URI: s3://{os.getenv('AWS_S3_BUCKET__BATCH_AUDIO')}/{transcript}")
    return transcript