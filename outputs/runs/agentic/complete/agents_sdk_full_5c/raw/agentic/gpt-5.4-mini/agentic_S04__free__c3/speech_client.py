from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Union

import assemblyai as aai


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    default_language_code: Optional[str] = None

    @classmethod
    def from_env(cls) -> "SpeechClientConfig":
        api_key = os.environ.get("ASSEMBLYAI_API_KEY")
        if not api_key:
            raise RuntimeError("ASSEMBLYAI_API_KEY is required for AssemblyAI integrations")
        return cls(api_key=api_key, default_language_code=os.environ.get("SPEECH_LANGUAGE_CODE"))


def build_assemblyai_client(config: Optional[SpeechClientConfig] = None) -> aai.Client:
    resolved = config or SpeechClientConfig.from_env()
    aai.settings.api_key = resolved.api_key
    return aai.Client()


def resolve_audio_source(*, audio_path: Optional[str] = None, audio_url: Optional[str] = None) -> Union[str, Path]:
    if audio_path and audio_url:
        raise ValueError("Provide either audio_path or audio_url, not both")
    if audio_path:
        return Path(audio_path)
    if audio_url:
        return audio_url
    raise ValueError("An audio_path or audio_url must be provided")
