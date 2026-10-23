from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from speech_models import SynthesisResponse, coerce_output_path, ensure_bytes


def save_audio(
    response: SynthesisResponse, destination: str | Path | BinaryIO
) -> str | Path:
    audio_bytes = ensure_bytes(response.audio_bytes)
    if hasattr(destination, "write"):
        destination.write(audio_bytes)
        return getattr(destination, "name", "<memory>")
    output_path = coerce_output_path(destination, response.content_type)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(audio_bytes)
    return output_path
