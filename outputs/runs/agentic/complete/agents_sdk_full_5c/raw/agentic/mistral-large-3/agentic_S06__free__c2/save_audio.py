from typing import Union
import io
from pathlib import Path
from google.cloud import storage

def save_audio_locally(audio_bytes: bytes, output_path: Union[str, Path]) -> None:
    """
    Writes synthesized speech audio to a local file.
    """
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

def save_audio_to_gcs(audio_bytes: bytes, bucket_name: str, blob_name: str) -> None:
    """
    Writes synthesized speech audio to Google Cloud Storage.
    """
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")