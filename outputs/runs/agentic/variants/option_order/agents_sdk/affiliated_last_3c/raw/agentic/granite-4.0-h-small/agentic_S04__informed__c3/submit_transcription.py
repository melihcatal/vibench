import os
import boto3
from speech_client import get_transcribe_client

def submit_transcription(file_path, transcript_job_name):
    # Use Amazon Transcribe as the concrete provider
    client = get_transcribe_client()
    # Submit a batch job for transcription
    response = client.start_transcription_job(
        TranscriptionJobName=transcript_job_name,
        Media={'MediaFileUri': f's3://{os.getenv("AWS_S3_BUCKET__BATCH_AUDIO")}/{file_path}"},
        MediaFormat='mp3',
        Settings={
            'LanguageCode': 'en-US',
        }
    )
    print(f"Transcription job submitted: {response['TranscriptionJob']['TranscriptionJobName']}")
    return response['TranscriptionJob']['TranscriptionJobName']