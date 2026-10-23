import os
from google.cloud import storage

def save_audio_local(audio_bytes: bytes, local_path: str) -> None:
    """Saves audio bytes to a local file."""
    with open(local_path, "wb") as out:
        out.write(audio_bytes)

def save_audio_gcs(audio_bytes: bytes, bucket_name: str, blob_name: str) -> None:
    """Uploads audio bytes to a Google Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.upload_from_string(audio_bytes)
    print(f"Audio content uploaded to gs://{bucket_name}/{blob_name}")
