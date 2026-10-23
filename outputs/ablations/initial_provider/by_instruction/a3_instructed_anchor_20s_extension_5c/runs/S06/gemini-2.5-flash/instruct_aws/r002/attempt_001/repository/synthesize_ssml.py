import boto3
import os
from typing import BinaryIO

def synthesize_ssml_aws(ssml_text: str, voice_id: str = "Joanna") -> BinaryIO:
    """
    Synthesizes SSML text to an audio byte stream using AWS Polly.
    """
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
        region_name=os.environ.get("AWS_REGION", "us-east-1"),
    )
    response = polly_client.synthesize_speech(
        Text=ssml_text, OutputFormat="mp3", VoiceId=voice_id, TextType="ssml"
    )
    return response["AudioStream"]
