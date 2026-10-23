from google.cloud import storage
from typing import Optional, Union
from io import BytesIO
import os


def save_audio(
    audio_bytes: bytes,
    local_path: Optional[str] = None,
    bucket_name: Optional[str] = None,
    object_name: Optional[str] = None,
) -> Union[str, BytesIO]:
    if local_path:
        with open(local_path, "wb") as f:
            f.write(audio_bytes)
        return local_path
    elif bucket_name and object_name:
        client = storage.Client(project=os.getenv("GOOGLE_CLOUD_PROJECT"))
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(object_name)
        blob.upload_from_string(audio_bytes, content_type="audio/mpeg")
        return (
            blob.public_url if blob.public_url else f"gs://{bucket_name}/{object_name}"
        )
    else:
        bio = BytesIO(audio_bytes)
        return bio
