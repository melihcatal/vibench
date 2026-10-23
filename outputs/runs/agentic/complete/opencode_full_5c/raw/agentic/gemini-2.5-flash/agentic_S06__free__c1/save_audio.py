from google.cloud import storage
import os


def save_audio_to_gcs(
    bucket_name: str, destination_blob_name: str, audio_content: bytes
):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(audio_content, content_type="audio/mpeg")
    return blob.public_url


def save_audio_to_file(file_path: str, audio_content: bytes):
    with open(file_path, "wb") as out:
        out.write(audio_content)
