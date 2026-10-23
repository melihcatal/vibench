import os
import boto3
from botocore.config import Config


def get_speech_client():
    """
    Get AWS Transcribe client with configuration.

    Returns:
        boto3 Transcribe client
    """
    # Configure AWS credentials from environment variables
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    # Create boto3 session
    session = boto3.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )

    # Create Transcribe client with configuration
    config = Config(retries={"max_attempts": 3, "mode": "standard"})

    return session.client("transcribe", config=config)


def validate_audio_file(file_path: str) -> bool:
    """
    Validate audio file format for AWS Transcribe.

    Args:
        file_path: Path to audio file

    Returns:
        True if valid, False otherwise
    """
    supported_formats = ["mp3", "mp4", "wav", "flac", "ogg", "amr", "webm"]

    if not os.path.exists(file_path):
        return False

    file_extension = file_path.split(".")[-1].lower()
    return file_extension in supported_formats


def get_supported_languages():
    """
    Get list of languages supported by AWS Transcribe.

    Returns:
        List of language codes
    """
    return [
        "en-US",
        "en-GB",
        "en-AU",
        "en-IN",
        "es-US",
        "es-ES",
        "fr-FR",
        "fr-CA",
        "de-DE",
        "it-IT",
        "ja-JP",
        "ko-KR",
        "pt-BR",
        "zh-CN",
    ]
