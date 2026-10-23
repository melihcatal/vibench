from __future__ import annotations

from pathlib import Path
from typing import Union

from synthesize_text import synthesize_text
from synthesize_ssml import synthesize_ssml


def save_audio(audio: bytes, output_path: Union[str, Path]) -> Path:
    path = Path(output_path)
    path.write_bytes(audio)
    return path


def synthesize_and_save_text(text: str, output_path: Union[str, Path], language_code: str = "en-US", voice_name: str | None = None) -> Path:
    return save_audio(synthesize_text(text=text, language_code=language_code, voice_name=voice_name), output_path)


def synthesize_and_save_ssml(ssml: str, output_path: Union[str, Path], language_code: str = "en-US", voice_name: str | None = None) -> Path:
    return save_audio(synthesize_ssml(ssml=ssml, language_code=language_code, voice_name=voice_name), output_path)
