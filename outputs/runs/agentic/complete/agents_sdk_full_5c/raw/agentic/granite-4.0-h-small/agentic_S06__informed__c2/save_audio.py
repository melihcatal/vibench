from typing import BinaryIO, Optional

from .speech_client import get_client
from .speech_models import SynthesisResult


def save_audio(result: SynthesisResult, target: str, fmt: str = "mp3") -> None:
    """Write synthesized speech to a local file or a supported object store path.

    - If `target` contains a schema (e.g., `gs://bucket/file.mp3`), upload via the cloud
      provider's SDK.  For Google Cloud storage we use `google-cloud-storage`.
    - Otherwise write to a local file.
    """
    client = get_client()
    bucket_name, blob_name = client.resolve_path(target)
    if bucket_name:
        # Provider‑specific upload (Google Cloud Storage example)
        bucket = client.storage_client.bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(result.audio_content, content_type=f"audio/{fmt}")
    else:
        # Simple local file write
        with open(target, "wb") as f:
            f.write(result.audio_content)
