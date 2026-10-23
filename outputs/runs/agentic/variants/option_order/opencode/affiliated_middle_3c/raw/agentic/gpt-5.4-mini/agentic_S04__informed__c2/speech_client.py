import os
from typing import Optional

import assemblyai as aai


def get_api_key() -> str:
    return os.getenv("ASSEMBLYAI_API_KEY", "")


def configure() -> None:
    key = get_api_key()
    if key:
        aai.settings.api_key = key


def create_transcriber() -> aai.Transcriber:
    configure()
    return aai.Transcriber()


def resolve_audio_source(
    audio_url: Optional[str] = None, audio_file: Optional[str] = None
) -> str:
    if audio_url:
        return audio_url
    if audio_file:
        return audio_file
    raise ValueError("audio_url or audio_file is required")
