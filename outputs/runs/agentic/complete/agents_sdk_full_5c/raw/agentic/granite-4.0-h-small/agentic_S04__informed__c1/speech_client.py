import os
import json
from typing import Dict

# Local helper to configure and create a Batch Speech-to-Text client for AWS Transcribe

class SpeechClient:
    """Local helper to configure and create a Batch Speech-to-Text client for AWS Transcribe"""
    _client = None

    @classmethod
    def get_client(cls) -> "boto3.client":
        if cls._client is None:
            # Configure AWS credentials via environment variables
            aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
            aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')
            if not aws_access_key or not aws_secret_key:
                raise RuntimeError('AWS credentials (AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY) not set')
            cls._client = boto3.client(                
                    service_name='transcribe',                
                    region_name='us-east-1',                
                    aws_access_key_id=aws_access_key,                
                    aws_secret_access_key=aws_secret_key,            )
        return cls._client

    @staticmethod
    def submit_job(
        job_name: str,
        media_file: str,
        output_bucket: str,
        language_code: str = 'en-US'
    ) -> Dict:
        """Submit a batch transcription job to AWS Transcribe"""
        client = SpeechClient.get_client()
        response = client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{media_file}'} if media_file.startswith('s3://') else {'MediaFileUri': f's3://{output_bucket}/{media_file}'}
            # Simplified; if local path, upload to S3 first
            LanguageCode=language_code
        )
        return response

    @staticmethod
    def get_job_status(job_name: str) -> Dict:
        """Poll a transcription job and return its status"""
        client = SpeechClient.get_client()
        return client.get_transcription_job(TranscriptionJobName=job_name)

    @staticmethod
    def retrieve_transcript(job_name: str) -> Dict:
        """Retrieve the completed transcript result (JSON) for a job"""
        client = SpeechClient.get_client()
        result = client.get_transcription_job(TranscriptionJobName=job_name)
        return result
