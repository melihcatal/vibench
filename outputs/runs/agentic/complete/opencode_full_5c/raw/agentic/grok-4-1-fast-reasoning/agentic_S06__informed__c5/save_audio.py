from google.cloud import storage
import os


def save_audio(
    audio_bytes: bytes, path: str, bucket_name: str = None, local: bool = True
):
    if local:
        with open(path, "wb") as f:
            f.write(audio_bytes)
    else:
        if not bucket_name:
            bucket_name = os.getenv("GCS_BUCKET_NAME")
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(path)
        blob.upload_from_string(audio_bytes, content_type="audio/wav")
