import os
from google.cloud import storage


def save_audio_to_file(audio_bytes, output_path):
    """Write synthesized speech audio to a local file."""
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    return output_path


def save_audio_to_gcs(audio_bytes, bucket_name, blob_name):
    """Write synthesized speech audio to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")

    return f"gs://{bucket_name}/{blob_name}"


def save_audio(audio_bytes, output_path=None, bucket_name=None, blob_name=None):
    """Save audio to either local file or Google Cloud Storage."""
    if output_path:
        return save_audio_to_file(audio_bytes, output_path)
    elif bucket_name and blob_name:
        return save_audio_to_gcs(audio_bytes, bucket_name, blob_name)
    else:
        raise ValueError(
            "Either output_path or (bucket_name and blob_name) must be provided"
        )
