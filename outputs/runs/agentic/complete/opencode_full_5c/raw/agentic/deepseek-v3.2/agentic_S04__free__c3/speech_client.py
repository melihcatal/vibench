import os
import boto3
from botocore.config import Config
from typing import Optional


def get_speech_client():
    """
    Get AWS Transcribe client with configuration.

    Returns:
        boto3 Transcribe client
    """
    aws_region = os.environ.get("AWS_REGION", "us-east-1")
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    if not aws_access_key_id or not aws_secret_access_key:
        raise EnvironmentError(
            "AWS credentials not found. Please set AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables."
        )

    config = Config(
        region_name=aws_region, retries={"max_attempts": 3, "mode": "standard"}
    )

    return boto3.client(
        "transcribe",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        config=config,
    )


def validate_audio_file(file_path: str) -> tuple[bool, str]:
    """
    Validate audio file format and size.

    Args:
        file_path: Path to audio file

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not os.path.exists(file_path):
        return False, f"File not found: {file_path}"

    valid_extensions = [".mp3", ".mp4", ".wav", ".flac", ".ogg", ".amr", ".webm"]
    file_ext = os.path.splitext(file_path)[1].lower()

    if file_ext not in valid_extensions:
        return (
            False,
            f"Unsupported audio format: {file_ext}. Supported: {', '.join(valid_extensions)}",
        )

    max_size_mb = 100
    file_size_mb = os.path.getsize(file_path) / (1024 * 1024)

    if file_size_mb > max_size_mb:
        return False, f"File too large: {file_size_mb:.2f}MB. Maximum: {max_size_mb}MB"

    return True, ""


def get_supported_languages() -> list[str]:
    """
    Get list of supported language codes for AWS Transcribe.

    Returns:
        List of language codes
    """
    return [
        "en-US",
        "en-GB",
        "en-AU",
        "es-US",
        "es-ES",
        "fr-FR",
        "fr-CA",
        "de-DE",
        "it-IT",
        "pt-BR",
        "ja-JP",
        "ko-KR",
        "zh-CN",
        "ar-SA",
        "ru-RU",
        "hi-IN",
    ]


def format_job_name(audio_file_path: str, prefix: str = "transcription") -> str:
    """
    Generate a unique job name for AWS Transcribe.

    Args:
        audio_file_path: Path to audio file
        prefix: Job name prefix

    Returns:
        Unique job name
    """
    import uuid
    import time

    base_name = os.path.basename(audio_file_path)
    safe_name = "".join(c if c.isalnum() else "_" for c in base_name)
    timestamp = int(time.time())
    unique_id = str(uuid.uuid4())[:8]

    return f"{prefix}_{safe_name}_{timestamp}_{unique_id}"[:100]
