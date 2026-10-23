from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from google.cloud import storage

from speech_models import SynthesisResult


WritableTarget = Union[str, Path, BinaryIO]


def save_audio(result: SynthesisResult, target: WritableTarget, content_type: str = "audio/mpeg") -> str:
    if hasattr(target, "write"):
        target.write(result.audio_bytes)
        return getattr(target, "name", "<stream>")

    target_str = str(target)
    if target_str.startswith("gs://"):
        bucket_name, blob_name = target_str[5:].split("/", 1)
        client = storage.Client()
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(result.audio_bytes, content_type=content_type)
        return target_str

    path = Path(target_str)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result.audio_bytes)
    return str(path)
