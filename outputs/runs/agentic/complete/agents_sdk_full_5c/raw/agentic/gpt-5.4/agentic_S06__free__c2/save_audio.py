from __future__ import annotations

from pathlib import Path

import boto3


def save_audio(audio_bytes: bytes, destination: str, *, content_type: str = "audio/mpeg") -> str:
    if destination.startswith("s3://"):
        bucket_and_key = destination[5:]
        bucket, key = bucket_and_key.split("/", 1)
        s3 = boto3.client("s3")
        s3.put_object(Bucket=bucket, Key=key, Body=audio_bytes, ContentType=content_type)
        return destination

    path = Path(destination)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(audio_bytes)
    return str(path)
