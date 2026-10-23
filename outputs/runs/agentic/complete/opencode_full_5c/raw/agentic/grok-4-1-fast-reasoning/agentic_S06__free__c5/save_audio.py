import boto3
from typing import Optional, Union


def save_audio(
    audio_bytes: bytes,
    destination: Union[str, None] = None,
    bucket: Optional[str] = None,
    key: Optional[str] = None,
):
    if destination:
        # Save to local file
        with open(destination, "wb") as f:
            f.write(audio_bytes)
        return
    if bucket and key:
        s3_client = boto3.client("s3")
        s3_client.put_object(
            Bucket=bucket, Key=key, Body=audio_bytes, ContentType="audio/mpeg"
        )
        return
    raise ValueError(
        "Must provide either 'destination' for local file or 'bucket' and 'key' for S3."
    )
