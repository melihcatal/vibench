import os
import boto3
from speech_client import SpeechClient, BatchTranscriptionConfig

# Amazon Transcribe example with diarization support
client = SpeechClient(service="Amazon Transcribe")


def request_diarized_transcription(
    audio_file_path: str, job_name: str = None, max_speakers: int = 2
):
    """Submit a batch transcription job with speaker diarization.

    Args:
        audio_file_path (str): Path to the audio file.
        job_name (str, optional): Custom job name. Defaults to None.
        max_speakers (int): Maximum number of speakers to identify.

    Returns:
        dict: Response containing job metadata including speaker labels.
    """
    region = os.getenv("AWS_REGION", "us-east-1")
    credentials = {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
    }
    for key in credentials.values():
        if not key:
            raise RuntimeError(
                "Missing AWS credentials. Set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY."
            )
    config = BatchTranscriptionConfig(
        audio_file_path=audio_file_path,
        job_name=job_name,
        region=region,
        enable_diarization=True,
        max_speakers=max_speakers,
    )
    return client.submit_batch_transcription(config)
