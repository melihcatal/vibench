from google.cloud import storage
from typing import Optional
import io

def save_audio(
    audio_content: bytes,
    destination: str,
    bucket_name: Optional[str] = None,
    content_type: str = "audio/mpeg"
) -> None:
    if bucket_name:
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(destination)
        blob.upload_from_string(audio_content, content_type=content_type)
        print(f"Uploaded to gs://{bucket_name}/{destination}")
    else:
        with open(destination, "wb") as f:
            f.write(audio_content)
        print(f"Saved to local file: {destination}")

def save_audio_to_buffer(audio_content: bytes) -> io.BytesIO:
    buffer = io.BytesIO(audio_content)
    buffer.seek(0)
    return buffer
