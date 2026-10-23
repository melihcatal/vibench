import os
from speech_models import SynthesisResponse
from typing import Union
import boto3


def save_audio_locally(audio_response: SynthesisResponse, file_path: str) -> None:
    """Write synthesized speech audio to a local file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "wb") as audio_file:
        audio_file.write(audio_response.audio_content)


def save_audio_to_s3(audio_response: SynthesisResponse, bucket_name: str, object_key: str) -> None:
    """Write synthesized speech audio to an S3 object using AWS S3."""
    s3_client = boto3.client("s3")
    s3_client.put_object(
        Bucket=bucket_name,
        Key=object_key,
        Body=audio_response.audio_content
    )