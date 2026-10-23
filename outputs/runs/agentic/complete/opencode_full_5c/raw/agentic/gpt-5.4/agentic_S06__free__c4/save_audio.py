from __future__ import annotations

from pathlib import Path

from speech_models import AudioResult, normalize_output_path


def save_audio(result: AudioResult, destination: str | Path) -> Path:
    output_path = normalize_output_path(destination)
    output_path.write_bytes(result.audio_bytes)
    return output_path
