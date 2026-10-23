import os
from typing import Dict, Any

import boto3
from botocore.exceptions import ClientError


def generate_speech_with_polly(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> Dict[str, Any]:
    """
    Generate spoken briefings from text using Amazon Polly.
    """
    client = boto3.client(
        service_name="polly",
        region_name=os.getenv("AWS_REGION", "us-west-2"),
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )

    try:
        response = client.synthesize_speech(
            Text=text, VoiceId=voice_id, OutputFormat=output_format
        )

        return {
            "audio_stream": response["AudioStream"].read(),
            "content_type": response["ContentType"],
            "request_characters": len(text),
            "provider": "aws_polly",
        }
    except ClientError as e:
        raise Exception(f"Failed to generate speech: {e}")
