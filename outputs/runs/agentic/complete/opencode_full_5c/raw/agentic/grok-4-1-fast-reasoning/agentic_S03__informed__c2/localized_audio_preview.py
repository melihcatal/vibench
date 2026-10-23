import os
import boto3
from typing import Optional


def generate_localized_audio_preview(
    text: str,
    voice_id: str = "Joanna",
    language_code: str = "en-US",
    output_format: str = "mp3",
) -> bytes:
    polly_client = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
    )
    response = polly_client.synthesize_speech(
        Text=text,
        VoiceId=voice_id,
        LanguageCode=language_code,
        OutputFormat=output_format,
    )
    if "AudioStream" in response:
        return response["AudioStream"].read()
    else:
        raise ValueError(f"Unable to synthesize speech: {response}")
