import os
import boto3
from speech_client import SpeechClient, BatchTranscriptionConfig

# Amazon Transcribe example
client = SpeechClient(service="Amazon Transcribe")


def submit_transcription(audio_file_path: str, job_name: str = None):
    """Submit an audio file for batch transcription using Amazon Transcribe.

    Args:
        audio_file_path (str): Path to the audio file.
        job_name (str, optional): Custom job name. Defaults to None.

    Returns:
        dict: Response from Amazon Transcribe containing job metadata.
    """
    # Load configuration from env or defaults
    region = os.getenv("AWS_REGION", "us-east-1")
    credentials = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
    # Ensure required credentials are present
    for key in credentials.values():
        if not key:
            raise RuntimeError(
                "Missing AWS credentials. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )
    # Prepare payload using helper
    config = BatchTranscriptionConfig(
        audio_file_path=audio_file_path,
        job_name=job_name,
        region=region,
    )
    return client.submit_batch_transcription(config)
