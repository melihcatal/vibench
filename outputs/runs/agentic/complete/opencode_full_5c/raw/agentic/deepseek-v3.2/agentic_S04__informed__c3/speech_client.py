import os
import boto3
from botocore.config import Config
from typing import Optional


def get_speech_client():
    """
    Create and return an Amazon Transcribe client.

    Returns:
        boto3 Transcribe client
    """
    # Configure AWS credentials from environment
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY environment variables."
        )

    # Create client with configuration
    config = Config(
        region_name=aws_region, retries={"max_attempts": 3, "mode": "standard"}
    )

    return boto3.client(
        "transcribe",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=config,
    )


def get_s3_client():
    """
    Create and return an S3 client for audio file storage.

    Returns:
        boto3 S3 client
    """
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    aws_region = os.environ.get("AWS_REGION", "us-east-1")

    if not aws_access_key_id or not aws_secret_access_key:
        raise ValueError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and "
            "AWS_SECRET_ACCESS_KEY environment variables."
        )

    return boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=aws_region,
    )


def validate_audio_file(file_path: str) -> bool:
    """
    Validate that the audio file exists and is in a supported format.

    Args:
        file_path: Path to audio file

    Returns:
        True if valid, False otherwise
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    # Check file extension
    supported_extensions = {".wav", ".mp3", ".mp4", ".flac", ".ogg", ".amr", ".webm"}
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext not in supported_extensions:
        print(f"Unsupported file format: {file_ext}. Supported: {supported_extensions}")
        return False

    # Check file size (Amazon Transcribe has limits)
    file_size = os.path.getsize(file_path)
    max_size = 2 * 1024 * 1024 * 1024  # 2GB

    if file_size > max_size:
        print(f"File too large: {file_size} bytes. Max: {max_size} bytes")
        return False

    return True


def get_supported_languages() -> list:
    """
    Return list of supported language codes for transcription.

    Returns:
        List of language codes
    """
    # Amazon Transcribe supported languages (partial list)
    return [
        "en-US",
        "en-GB",
        "en-AU",
        "en-IN",  # English variants
        "es-US",
        "es-ES",  # Spanish
        "fr-FR",
        "fr-CA",  # French
        "de-DE",  # German
        "it-IT",  # Italian
        "pt-BR",
        "pt-PT",  # Portuguese
        "ja-JP",  # Japanese
        "ko-KR",  # Korean
        "zh-CN",
        "zh-TW",  # Chinese
        "ar-SA",  # Arabic
        "ru-RU",  # Russian
        "hi-IN",  # Hindi
    ]


def get_default_bucket() -> str:
    """
    Get the default S3 bucket name for audio storage.

    Returns:
        Bucket name
    """
    return os.environ.get("AWS_TRANSCRIBE_BUCKET", "transcription-audio-bucket")
