import os
import time
import json
import boto3
from typing import Dict, Any, Optional

S3_BUCKET = os.getenv('S3_TRANSCRIBE_BUCKET', 'transcribe-bucket')

def get_transcribe_client() -> boto3.client:
    return boto3.client('transcribe')

def get_s3_client() -> boto3.client:
    return boto3.client('s3')

def upload_audio_to_s3(local_file: str, s3_key: str) -> str:
    s3 = get_s3_client()
    s3.upload_file(local_file, S3_BUCKET, s3_key)
    return f's3://{S3_BUCKET}/{s3_key}'

def wait_for_completion(job_name: str, poll_interval: int = 30) -> Dict[str, Any]:
    client = get_transcribe_client()
    while True:
        response = client.get_transcription_job(TranscriptionJobName=job_name)
        status = response['TranscriptionJob']['TranscriptionJobStatus']
        if status in ['COMPLETED', 'FAILED']:
            if status == 'FAILED':
                reason = response['TranscriptionJob'].get('FailureReason', 'Unknown')
                raise RuntimeError(f'Transcription failed: {reason}')
            return response['TranscriptionJob']
        time.sleep(poll_interval)

def download_transcript_json(transcribe_job: Dict[str, Any]) -> Dict[str, Any]:
    transcript_uri = transcribe_job['Transcript']['TranscriptFileUri']
    parts = transcript_uri.replace('s3://', '').split('/', 1)
    bucket = parts[0]
    key = parts[1]
    s3 = get_s3_client()
    obj = s3.get_object(Bucket=bucket, Key=key)
    return json.loads(obj['Body'].read().decode('utf-8'))