import os
from pathlib import Path


def save_audio_to_file(audio_bytes: bytes, output_path: str) -> str:
    """Write synthesized speech audio to a local file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "wb") as f:
        f.write(audio_bytes)

    return str(output_path.absolute())


def save_audio_to_gcs(audio_bytes: bytes, bucket_name: str, blob_name: str) -> str:
    """Write synthesized speech audio to Google Cloud Storage."""
    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")

    return f"gs://{bucket_name}/{blob_name}"
