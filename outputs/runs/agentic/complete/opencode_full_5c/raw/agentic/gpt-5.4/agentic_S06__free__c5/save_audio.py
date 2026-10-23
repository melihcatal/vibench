from __future__ import annotations

from pathlib import Path

from speech_models import SynthesisResponse


def save_audio(response: SynthesisResponse, destination: str | Path) -> Path:
    output_path = Path(destination)
    output_path.write_bytes(response.audio_bytes)
    return output_path
