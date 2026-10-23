from google.cloud import storage
import os
from typing import Optional


def save_audio(
    audio_content: bytes, path: str, bucket_name: Optional[str] = None
) -> str:
    if bucket_name:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path)
        blob.upload_from_string(data=audio_content, content_type="audio/mpeg")
        return f"gs://{bucket_name}/{path}"
    else:
        with open(path, "wb") as f:
            f.write(audio_content)
        return path
