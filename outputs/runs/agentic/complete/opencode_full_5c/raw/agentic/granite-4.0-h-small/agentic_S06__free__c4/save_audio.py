# [SAME-SCENARIO] save_audio.py
# Writes synthesized speech audio to a local file or object

from pathlib import Path
import os


def save_audio(audio_bytes: bytes, destination: str) -> Path:
    """
    Saves raw audio bytes to a local file or to cloud storage.
    For local files, destination is a filepath.
    For cloud storage, set environment variable CLOUD_PROVIDER and use appropriate SDK.
    """
    if destination.startswith("gs://"):
        # Example: Google Cloud Storage
        from google.cloud import storage

        bucket_name, blob_name = destination[5:].split("/", 1)
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(audio_bytes, content_type="audio/l16")
        return Path(blob.name)
    else:
        # Local file path
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio_bytes)
        return path
