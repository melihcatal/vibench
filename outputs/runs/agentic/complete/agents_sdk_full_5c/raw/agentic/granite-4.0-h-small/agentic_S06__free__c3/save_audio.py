# save_audio.py
# [SAME-SCENARIO]
# Writes synthesized speech audio bytes to a local file or cloud object storage.

import os
from pathlib import Path

# Local helper utilities
from speech_client import get_audio_bytes
from speech_models import AudioFormat

def save_audio(audio_bytes: bytes, destination: str, format: AudioFormat = AudioFormat.MP3):
    """Save synthesized speech audio.
    Args:
        audio_bytes: raw audio bytes (e.g., MP3).
        destination: path to local file or GCS URI (gs://bucket/path).
        format: expected encoding (defaults to MP3).
    """
    if destination.startswith("gs://"):
        # Example: using google-cloud-storage client (requires GOOGLE_APPLICATION_CREDENTIALS)
        from google.cloud import storage
        bucket_name, blob_path = destination[5:].split("/", 1)
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_path)
        blob.upload_from_string(audio_bytes, content_type="audio/mpeg")
        print(f"Audio saved to GCS: gs://{bucket_name}/{blob_path}")
    else:
        # Local file write
        path = Path(destination)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(audio_bytes)
        print(f"Audio saved locally: {path.resolve()}")
