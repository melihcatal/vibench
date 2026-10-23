import boto3
from typing import Optional
import json


def generate_spoken_brief(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> bytes:
    """
    Generate a spoken brief from the model output using Amazon Polly.
    """
    client = boto3.client("polly")

    response = client.synthesize_speech(
        Text=text, VoiceId=voice_id, OutputFormat=output_format, Engine="neural"
    )

    return response["AudioStream"].read()
