import os
from io import BytesIO
from google.cloud import storage

def save_audio_to_local(audio_bytes: bytes, output_path: str) -> None:
    """
    Writes synthesized speech audio to a local file.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(audio_bytes)

def save_audio_to_gcs(audio_bytes: bytes, bucket_name: str, blob_name: str) -> None:
    """
    Writes synthesized speech audio to Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")