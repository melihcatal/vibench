import os
from google.cloud import storage


def save_audio_to_file(audio_bytes, filepath):
    """Write synthesized speech audio to a local file."""
    with open(filepath, "wb") as audio_file:
        audio_file.write(audio_bytes)
    return filepath


def save_audio_to_gcs(audio_bytes, bucket_name, destination_blob_name):
    """Write synthesized speech audio to Google Cloud Storage."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")

    return f"gs://{bucket_name}/{destination_blob_name}"


def save_audio_to_object_storage(audio_bytes, provider="local", **kwargs):
    """Write audio to various storage providers."""
    if provider == "local":
        return save_audio_to_file(audio_bytes, kwargs.get("filepath", "output.mp3"))
    elif provider == "gcs":
        return save_audio_to_gcs(
            audio_bytes,
            kwargs.get("bucket_name", "tts-audio-bucket"),
            kwargs.get("destination_blob_name", "output.mp3"),
        )
    else:
        raise ValueError(f"Unsupported provider: {provider}")
