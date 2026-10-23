from google.cloud import storage
import os


def save_audio_to_gcs(audio_bytes: bytes, destination_blob_name: str):
    """Uploads audio bytes to a Google Cloud Storage bucket."""
    bucket_name = os.environ.get("GCS_BUCKET_NAME")
    if not bucket_name:
        raise ValueError("GCS_BUCKET_NAME environment variable not set.")

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_string(audio_bytes, content_type="audio/mpeg")


def save_audio_to_local_file(audio_bytes: bytes, file_path: str):
    """Saves audio bytes to a local file."""
    with open(file_path, "wb") as out:
        out.write(audio_bytes)


def save_audio(audio_bytes: bytes, file_path: str, is_local: bool = True):
    """Saves audio to a local file or GCS."""
    if is_local:
        save_audio_to_local_file(audio_bytes, file_path)
    else:
        save_audio_to_gcs(audio_bytes, file_path)
