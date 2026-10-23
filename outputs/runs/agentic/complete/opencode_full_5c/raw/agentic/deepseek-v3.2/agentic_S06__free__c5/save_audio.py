import os
from pathlib import Path


def save_audio_to_file(audio_bytes, filepath):
    """Write synthesized speech audio to a local file."""
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "wb") as audio_file:
        audio_file.write(audio_bytes)

    return str(filepath.absolute())


def save_audio_to_object_storage(audio_bytes, bucket_name, object_name):
    """Write synthesized speech audio to Google Cloud Storage."""
    from google.cloud import storage

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(object_name)

    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")

    return f"gs://{bucket_name}/{object_name}"
