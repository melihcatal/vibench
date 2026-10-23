import os
import boto3
from botocore.exceptions import ClientError
from typing import Optional


def generate_audio_preview(
    text: str, language_code: str, voice_id: str = "Joanna"
) -> bytes:
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get(
        "AWS_REGION", "us-east-1"
    )  # Default to us-east-1 if not set

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables must be set."
        )

    polly_client = boto3.client(
        "polly",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    try:
        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat="mp3",
            VoiceId=voice_id,  # e.g., 'Joanna' for English, 'Vicki' for German, 'Zhiyu' for Chinese
            LanguageCode=language_code,  # e.g., 'en-US', 'de-DE', 'cmn-CN'
        )

        if "AudioStream" in response:
            return response["AudioStream"].read()
        else:
            raise RuntimeError("Could not get audio stream from AWS Polly.")

    except ClientError as e:
        raise RuntimeError(f"AWS Polly error: {e}")
