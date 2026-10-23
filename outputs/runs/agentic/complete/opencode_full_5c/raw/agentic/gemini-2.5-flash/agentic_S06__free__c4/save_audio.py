from speech_client import get_gcs_client
from typing import Optional
from google.cloud import storage


def save_audio_to_gcs(
    audio_content: bytes,
    bucket_name: str,
    destination_blob_name: str,
    content_type: str = "audio/mpeg",
):  # Default to MP3
    client = get_gcs_client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_content, content_type=content_type)
    print(f"Audio uploaded to gs://{bucket_name}/{destination_blob_name}")
