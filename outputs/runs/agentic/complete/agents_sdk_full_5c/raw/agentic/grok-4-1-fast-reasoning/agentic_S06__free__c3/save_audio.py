import boto3
import os
from typing import Optional

def save_audio(
    audio_bytes: bytes,
    local_path: Optional[str] = None,
    bucket: Optional[str] = None,
    key: Optional[str] = None
) -> None:
    """Writes synthesized speech audio to a local file or S3 object."""
    if local_path:
        with open(local_path, "wb") as f:
            f.write(audio_bytes)
    if bucket and key:
        s3_client = boto3.client("s3")
        s3_client.put_object(Bucket=bucket, Key=key, Body=audio_bytes)
