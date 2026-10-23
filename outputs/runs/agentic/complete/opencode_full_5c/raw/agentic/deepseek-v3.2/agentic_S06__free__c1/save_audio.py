import os
from google.cloud import storage


def save_audio_to_file(audio_content, filepath):
    """Write synthesized speech audio to a local file."""
    with open(filepath, "wb") as out:
        out.write(audio_content)
    return filepath


def save_audio_to_gcs(audio_content, bucket_name, blob_name):
    """Write synthesized speech audio to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(audio_content, content_type="audio/mpeg")

    return f"gs://{bucket_name}/{blob_name}"
