import os
import boto3
from typing import Optional


def generate_platform_brief_audio(
    text: str, output_file: str, voice_id: str = "Joanna"
):
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
    if not access_key or not secret_key:
        raise ValueError("AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be set")
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key,
        region_name=region,
    )
    response = polly_client.synthesize_speech(
        Text=text, OutputFormat="mp3", VoiceId=voice_id, Engine="neural"
    )
    with open(output_file, "wb") as file:
        file.write(response["AudioStream"].read())
