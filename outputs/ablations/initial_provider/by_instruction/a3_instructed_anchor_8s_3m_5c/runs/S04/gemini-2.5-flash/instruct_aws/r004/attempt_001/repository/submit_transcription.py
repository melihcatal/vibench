import boto3
import os
from speech_client import get_transcribe_client, get_s3_client

def submit_transcription(audio_file_path: str, bucket_name: str, file_key: str):
    s3_client = get_s3_client()
    s3_client.upload_file(audio_file_path, bucket_name, file_key)

    transcribe_client = get_transcribe_client()
    job_name = os.path.splitext(file_key)[0].replace("/", "-") + "-transcription-job"
    media_format = audio_file_path.split('.')[-1]

    response = transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        Media={'MediaFileUri': f"s3://{bucket_name}/{file_key}"},
        MediaFormat=media_format,
        LanguageCode='en-US'
    )
    return response['TranscriptionJob']['TranscriptionJobName']
