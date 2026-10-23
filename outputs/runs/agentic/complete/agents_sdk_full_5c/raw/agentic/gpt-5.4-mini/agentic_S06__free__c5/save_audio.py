from __future__ import annotations

from pathlib import Path
from typing import Union

from speech_client import build_speech_client
from speech_models import AudioTarget

try:
    from google.cloud import texttospeech
except Exception:  # pragma: no cover
    texttospeech = None



def save_audio(audio_bytes: bytes, target: Union[str, Path, AudioTarget]) -> str:
    """Write synthesized audio to a local file path."""
    if texttospeech is None:
        raise RuntimeError("google-cloud-texttospeech is required for save_audio")
    path = Path(target.path if isinstance(target, AudioTarget) else target)
    path.write_bytes(audio_bytes)
    return str(path)
