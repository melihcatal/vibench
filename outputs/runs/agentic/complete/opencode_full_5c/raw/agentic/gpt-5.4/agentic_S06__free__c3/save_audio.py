from __future__ import annotations

from pathlib import Path

from google.cloud import storage

from speech_models import AudioResult


def save_audio(result: AudioResult, destination: str) -> str:
    if destination.startswith("gs://"):
        bucket_name, blob_name = destination[5:].split("/", 1)
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(
            result.audio_bytes, content_type=_content_type(result.audio_encoding)
        )
        return destination
    path = Path(destination)
    path.write_bytes(result.audio_bytes)
    return str(path)


def _content_type(audio_encoding: str) -> str:
    value = audio_encoding.upper()
    if value == "MP3":
        return "audio/mpeg"
    if value == "OGG_OPUS":
        return "audio/ogg"
    return "audio/wav"
