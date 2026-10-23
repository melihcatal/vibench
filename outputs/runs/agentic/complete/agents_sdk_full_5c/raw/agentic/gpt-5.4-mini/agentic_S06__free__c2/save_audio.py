from __future__ import annotations

from pathlib import Path
from typing import BinaryIO, Union

from google.cloud import texttospeech

from speech_client import get_client, load_speech_config
from speech_models import normalize_text


WritableTarget = Union[str, Path, BinaryIO]


def save_audio(text: str, target: WritableTarget, language_code: str | None = None, voice_name: str | None = None) -> int:
    client = get_client()
    config = load_speech_config()
    request = texttospeech.SynthesisInput(text=normalize_text(text))
    voice = texttospeech.VoiceSelectionParams(
        language_code=language_code or config.default_language_code,
        name=voice_name or config.default_voice_name or "",
    )
    audio_config = texttospeech.AudioConfig(audio_encoding=config.audio_encoding)
    response = client.synthesize_speech(input=request, voice=voice, audio_config=audio_config)
    data = response.audio_content
    if hasattr(target, "write"):
        target.write(data)
    else:
        Path(target).write_bytes(data)
    return len(data)
