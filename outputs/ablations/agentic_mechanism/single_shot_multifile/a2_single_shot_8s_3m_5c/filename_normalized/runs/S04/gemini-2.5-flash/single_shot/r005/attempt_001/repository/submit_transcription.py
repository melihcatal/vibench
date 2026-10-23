import os
import boto3
import uuid
from speech_client import get_transcribe_client, get_s3_client

def submit_transcription_job(audio_file_path: str, bucket_name: str, language_code: str = 'en-US') -> str:
    s3_client = get_s3_client()
    transcribe_client = get_transcribe_client()

    # Upload audio file to S3
    object_key = f"audio/{uuid.uuid4()}_{os.path.basename(audio_file_path)}"
    s3_client.upload_file(audio_file_path, bucket_name, object_key)
    audio_uri = f"s3://{bucket_name}/{object_key}"

    job_name = f"batch-transcript-{uuid.uuid4()}"

    transcribe_client.start_transcription_job(
        TranscriptionJobName=job_name,
        LanguageCode=language_code,
        MediaFormat=audio_file_path.split('.')[-1],
        Media={'MediaFileUri': audio_uri},
        OutputBucketName=bucket_name
    )
    return job_name