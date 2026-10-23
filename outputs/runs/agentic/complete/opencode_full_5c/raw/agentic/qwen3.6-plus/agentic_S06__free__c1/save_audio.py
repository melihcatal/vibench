from __future__ import annotations

import os
import io
from pathlib import Path

from speech_models import TTSResponse


FORMAT_EXTENSION_MAP = {
    "mp3": ".mp3",
    "opus": ".opus",
    "aac": ".aac",
    "flac": ".flac",
    "wav": ".wav",
    "pcm": ".pcm",
}


def save_audio(
    tts_response: TTSResponse,
    output_path: str | Path | None = None,
    format_override: str | None = None,
    overwrite: bool = False,
) -> str:
    if tts_response.audio_bytes is None or len(tts_response.audio_bytes) == 0:
        raise ValueError("No audio bytes to save")

    audio_bytes = tts_response.audio_bytes

    if output_path is not None:
        path = Path(output_path)
        if path.is_dir():
            ext = FORMAT_EXTENSION_MAP.get(
                format_override or tts_response.format, ".mp3"
            )
            path = path / f"speech_{tts_response.voice}{ext}"
        if path.exists() and not overwrite:
            raise FileExistsError(f"File already exists: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "wb") as f:
            f.write(audio_bytes)
        return str(path)

    ext = FORMAT_EXTENSION_MAP.get(format_override or tts_response.format, ".mp3")
    filename = f"speech_{tts_response.voice}_{tts_response.model}{ext}"
    with open(filename, "wb") as f:
        f.write(audio_bytes)
    return filename


def save_audio_to_buffer(
    tts_response: TTSResponse,
    format_override: str | None = None,
) -> io.BytesIO:
    if tts_response.audio_bytes is None or len(tts_response.audio_bytes) == 0:
        raise ValueError("No audio bytes to save")
    return io.BytesIO(tts_response.audio_bytes)
