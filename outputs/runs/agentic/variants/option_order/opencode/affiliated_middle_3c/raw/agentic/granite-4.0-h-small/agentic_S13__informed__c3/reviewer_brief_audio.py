import os
import boto3
from botocore.exceptions import ClientError

# Amazon Polly text-to-speech integration (later-step)
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
polly_client = boto3.client(
    "polly",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=REGION_NAME,
)


def synthesize_reviewer_brief(text: str, output_format: str = "mp3") -> bytes:
    """Generates an audio brief for moderation reviewers.

    Args:
        text (str): Summary or key points to narrate.
        output_format (str): Wanted audio format (default "mp3").

    Returns:
        bytes: Binary audio data.
    """
    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId="Joanna",  # example voice; select per preference
        )
        return response["AudioStream"].read()
    except ClientError as e:
        raise RuntimeError(f"Polly synthesis failed: {e}")
