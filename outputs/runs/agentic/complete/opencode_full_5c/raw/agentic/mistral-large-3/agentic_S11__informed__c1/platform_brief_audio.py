from typing import Optional
import os
import boto3
from .model_models import AudioRequest, AudioResponse


def platform_brief_audio(
    text: str, voice: Optional[str] = "Joanna", format: Optional[str] = "mp3"
) -> AudioResponse:
    """
    Generates spoken briefings from platform outputs using Amazon Polly.
    """
    polly = boto3.client(
        "polly",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "us-west-2"),
    )

    response = polly.synthesize_speech(Text=text, OutputFormat=format, VoiceId=voice)

    return AudioResponse(audio_content=response["AudioStream"].read(), format=format)
