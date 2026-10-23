import os
import tempfile
from google.cloud import storage


def save_audio_to_file(audio_content, filepath):
    """Write synthesized speech audio to a local file."""
    with open(filepath, "wb") as f:
        f.write(audio_content)
    return filepath


def save_audio_to_gcs(audio_content, bucket_name, blob_name):
    """Write synthesized speech audio to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(audio_content, content_type="audio/mpeg")

    return f"gs://{bucket_name}/{blob_name}"


def save_audio_to_temp_file(audio_content, suffix=".mp3"):
    """Write synthesized speech audio to a temporary file."""
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as f:
        f.write(audio_content)
        return f.name
