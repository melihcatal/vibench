import os
import requests

# AWS Polly environment variables
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

if not (AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY):
    raise RuntimeError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")

from boto3 import client as boto3_client

polly_client = boto3_client(
    "polly",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


def generate_speech(
    text: str, voice_id: str = "Matthew", output_format: str = "mp3"
) -> bytes:
    """Synthesizes speech from text using Amazon Polly.

    Returns raw audio bytes in the requested format."""
    response = polly_client.synthesize_speech(
        Text=text, VoiceId=voice_id, OutputFormat=output_format
    )
    # The response's 'AudioStream' is a streaming object; read bytes
    return response["AudioStream"].read()


def save_brief(text: str, file_path: str, voice_id: str = "Matthew") -> None:
    """Generates speech and writes to a file."""
    audio_bytes = generate_speech(text, voice_id)
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
