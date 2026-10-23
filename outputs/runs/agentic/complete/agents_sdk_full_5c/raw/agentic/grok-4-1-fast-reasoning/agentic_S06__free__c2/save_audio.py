import os
from typing import Optional
from google.cloud import storage

def save_audio_to_gcs(
    audio_content: bytes,
    bucket_name: str,
    blob_name: str,
    project_id: Optional[str] = None
) -> str:
    project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT must be set.")
    client = storage.Client(project=project_id)
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(
        audio_content,
        content_type="audio/mpeg"
    )
    blob.make_public()  # Optional
    return f"gs://{bucket_name}/{blob_name}"

def save_audio_to_file(
    audio_content: bytes,
    file_path: str
) -> None:
    with open(file_path, "wb") as f:
        f.write(audio_content)
