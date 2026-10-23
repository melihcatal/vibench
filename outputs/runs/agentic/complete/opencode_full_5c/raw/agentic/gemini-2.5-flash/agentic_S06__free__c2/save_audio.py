import os
from google.cloud import storage


def save_audio(
    audio_content: bytes, destination_path: str, bucket_name: Optional[str] = None
):
    """Writes synthesized speech audio to a local file or Google Cloud Storage object.

    If bucket_name is provided, saves to GCS. Otherwise, saves to a local file.
    """
    if bucket_name:
        # Save to Google Cloud Storage
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination_path)
        blob.upload_from_string(
            audio_content, content_type="audio/mpeg"
        )  # Assuming MP3 for common use
    else:
        # Save to local file
        with open(destination_path, "wb") as out_file:
            out_file.write(audio_content)
