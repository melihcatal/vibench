from __future__ import annotations

from pathlib import Path

from speech_models import AudioResult


def save_audio(result: AudioResult, destination: str | Path) -> Path:
    path = Path(destination)
    if path.suffix == "":
        path = path.with_suffix(f".{result.audio_format}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(result.audio_bytes)
    return path
