import os
import boto3
from typing import Optional, BinaryIO
from dataclasses import dataclass
from io import BytesIO


@dataclass
class AudioBriefResult:
    audio_data: bytes
    content_type: str
    voice_id: str
    raw_response: Optional[Dict] = None


def generate_platform_brief_audio(
    text: str, voice_id: str = "Joanna", output_format: str = "mp3"
) -> AudioBriefResult:
    """
    Generate spoken briefings from platform outputs using Amazon Polly.
    """
    aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
    aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    aws_region = os.getenv("AWS_REGION", "us-east-1")

    if not aws_access_key or not aws_secret_key:
        raise ValueError(
            "AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables are required"
        )

    try:
        polly_client = boto3.client(
            "polly",
            aws_access_key_id=aws_access_key,
            aws_secret_access_key=aws_secret_key,
            region_name=aws_region,
        )

        response = polly_client.synthesize_speech(
            Text=text,
            OutputFormat=output_format,
            VoiceId=voice_id,
            Engine="neural"
            if voice_id in ["Joanna", "Matthew", "Amy", "Brian"]
            else "standard",
        )

        audio_stream = response["AudioStream"].read()

        return AudioBriefResult(
            audio_data=audio_stream,
            content_type=f"audio/{output_format}",
            voice_id=voice_id,
            raw_response=response,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to generate audio with Amazon Polly: {e}")


def save_audio_to_file(audio_result: AudioBriefResult, filepath: str) -> None:
    """
    Save audio briefing to a file.
    """
    with open(filepath, "wb") as f:
        f.write(audio_result.audio_data)
