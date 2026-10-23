# [SAME-SCENARIO] save_audio.py

import os
from pathlib import Path


def write_audio_to_file(
    audio_bytes: bytes, file_path: str, format: str = "mp3"
) -> Path:
    """Writes synthesized speech audio to a local file.

    Args:
        audio_bytes: Raw audio bytes from TTS response.
        file_path: Destination path (e.g., "./output.mp3").
        format: Audio format identifier (used for extension only).

    Returns:
        Path of the saved file.
    """
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio_bytes)
    return path


def upload_to_object_storage(
    audio_bytes: bytes, bucket_name: str, object_key: str
) -> str:
    """Dummy helper to upload audio to an object store (e.g., AWS S3).

    Args:
        audio_bytes: Raw audio bytes.
        bucket_name: Bucket identifier.
        object_key: Key/Name within the bucket.

    Returns:
        Placeholder identifier (e.g., URL). Replace with real SDK call as needed.
    """
    # Replace the body with actual provider SDK calls (boto3 S3 client, etc.)
    return f"s3://{bucket_name}/{object_key}"
