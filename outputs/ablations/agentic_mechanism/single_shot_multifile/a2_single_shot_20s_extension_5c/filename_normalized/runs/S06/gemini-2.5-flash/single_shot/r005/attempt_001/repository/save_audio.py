import os
from google.cloud import storage

def save_audio_to_gcs(audio_bytes: bytes, destination_blob_name: str, bucket_name: str) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")

    return blob.public_url

def save_audio_to_local_file(audio_bytes: bytes, file_path: str):
    with open(file_path, "wb") as f:
        f.write(audio_bytes)
