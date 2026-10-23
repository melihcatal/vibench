
# [SAME-SCENARIO] partial_results.py
import json
from typing import Dict, Any

# Provider: Amazon Transcribe Streaming (boto3 SDK)
import boto3
import os

client = boto3.client(
    'transcribe',
    region_name=os.getenv('AWS_REGION', 'us-east-1'),
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
)

def lambda_handler(event, context):
    # Expected event format from AWS Lambda invocation of Transcribe job
    job_name = event['TranscriptionJobName']
    # Fetch job details
    response = client.get_transcription_job(TranscriptionJobName=job_name)
    job = response['TranscriptionJob']
    status = job['TranscriptionJobStatus']
    if status == 'COMPLETED':
        transcript = job['Transcript']['TranscriptFileUri']
        print('Transcription complete:', transcript)
    elif status == 'IN_PROGRESS':
        # Partial results are available via a separate API call or stream
        print('Partial results are being streamed...')
    else:
        print('Job status:', status)
    return {'status': status}
