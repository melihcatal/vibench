import os
import time
import json
import requests
from speech_client import get_transcribe_client, get_s3_client

def poll_transcription_job(job_name: str, poll_interval_seconds: int = 10) -> str:
    transcribe_client = get_transcribe_client()
    s3_client = get_s3_client()

    while True:
        response = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = response['TranscriptionJob']['TranscriptionJobStatus']

        if job_status == 'COMPLETED':
            transcript_file_uri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
            # The URI is like https://s3.REGION.amazonaws.com/BUCKET_NAME/JOB_NAME.json
            # We need to parse bucket and key from this URI
            uri_parts = transcript_file_uri.split('/')
            bucket_name = uri_parts[2].split('.')[0] # e.g., s3.us-east-1.amazonaws.com
            if bucket_name == 's3':
                bucket_name = uri_parts[3]
                object_key = '/'.join(uri_parts[4:])
            else:
                bucket_name = transcript_file_uri.split('/')[2].split('.')[0]
                object_key = '/'.join(transcript_file_uri.split('/')[3:])

            # Since AWS Transcribe often outputs to a public URL or requires signed URL, easier to download directly
            # However, if output bucket is specified, it saves there. Let's assume public URL download for simplicity
            # If private, would use s3_client.get_object. For now, direct HTTP GET.
            transcript_content = requests.get(transcript_file_uri).json()
            return transcript_content['results']['transcripts'][0]['transcript']
        elif job_status == 'FAILED':
            raise Exception(f"Transcription job {job_name} failed: {response['TranscriptionJob']['FailureReason']}")
        else:
            time.sleep(poll_interval_seconds)