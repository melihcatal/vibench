import io
import os
import boto3


def save_audio(
    audio_bytes: bytes,
    local_path: str = None,
    bucket: str = None,
    object_key: str = None,
) -> str | io.BytesIO:
    if local_path:
        with open(local_path, "wb") as f:
            f.write(audio_bytes)
        return local_path
    if bucket and object_key:
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
        )
        s3_client.put_object(Bucket=bucket, Key=object_key, Body=audio_bytes)
        return f"s3://{bucket}/{object_key}"
    return io.BytesIO(audio_bytes)
