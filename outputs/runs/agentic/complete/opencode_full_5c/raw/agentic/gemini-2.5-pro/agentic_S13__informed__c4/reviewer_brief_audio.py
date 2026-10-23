import os
import boto3
from botocore.exceptions import BotoCoreError, ClientError


def reviewer_brief_audio(text: str) -> bytes:
    try:
        # For this example, we assume credentials are configured in the environment
        # e.g., AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION
        polly_client = boto3.client("polly")
    except (BotoCoreError, ClientError) as e:
        raise ConnectionError(f"Could not create boto3 Polly client. Error: {e}")

    try:
        response = polly_client.synthesize_speech(
            VoiceId="Joanna", OutputFormat="mp3", Text=text, Engine="neural"
        )
        return response["AudioStream"].read()
    except (BotoCoreError, ClientError) as e:
        raise RuntimeError(f"Amazon Polly API call failed. Error: {e}")
