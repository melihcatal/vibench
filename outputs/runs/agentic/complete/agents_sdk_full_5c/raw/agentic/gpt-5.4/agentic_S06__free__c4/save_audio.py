from __future__ import annotations

from pathlib import Path

from google.cloud import storage

from speech_models import AudioArtifact


GOOGLE_CLOUD_STORAGE_PROVIDER = "storage.googleapis.com"


def save_audio_to_file(audio: AudioArtifact, destination_path: str) -> str:
    path = Path(destination_path)
    path.write_bytes(audio.content)
    return str(path)


def save_audio_to_gcs(audio: AudioArtifact, bucket_name: str, blob_name: str) -> str:
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_string(audio.content, content_type=_content_type_for_encoding(audio.encoding))
    return f"gs://{bucket_name}/{blob_name}"


def _content_type_for_encoding(encoding: str) -> str:
    normalized = (encoding or "").upper()
    if normalized == "MP3":
        return "audio/mpeg"
    if normalized == "LINEAR16":
        return "audio/wav"
    if normalized == "OGG_OPUS":
        return "audio/ogg"
    return "application/octet-stream"
