import os
from speech_client import get_s3_client

def save_audio_to_s3(audio_bytes: bytes, filename: str, s3_bucket_name: str) -> str:
    s3_client = get_s3_client()
    s3_client.put_object(
        Bucket=s3_bucket_name,
        Key=filename,
        Body=audio_bytes,
        ContentType='audio/mpeg'
    )
    return f"s3://{s3_bucket_name}/{filename}"
