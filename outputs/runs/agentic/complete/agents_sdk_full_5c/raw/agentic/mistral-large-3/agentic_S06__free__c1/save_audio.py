import io
from google.cloud import storage
from typing import Union
import os

def save_audio_to_file(audio_bytes: bytes, output_path: str) -> None:
    with open(output_path, "wb") as audio_file:
        audio_file.write(audio_bytes)

def save_audio_to_gcs(audio_bytes: bytes, bucket_name: str, destination_blob_name: str) -> None:
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")

def save_audio(audio_bytes: bytes, destination: str) -> None:
    if destination.startswith("gs://"):
        bucket_name, blob_name = destination[5:].split("/", 1)
        save_audio_to_gcs(audio_bytes, bucket_name, blob_name)
    else:
        save_audio_to_file(audio_bytes, destination)