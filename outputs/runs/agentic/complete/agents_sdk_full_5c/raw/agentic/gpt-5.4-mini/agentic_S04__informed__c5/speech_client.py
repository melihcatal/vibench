from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    language_code: Optional[str] = None
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True


def load_config() -> SpeechConfig:
    api_key = os.getenv("ASSEMBLYAI_API_KEY", "")
    if not api_key:
        raise RuntimeError("ASSEMBLYAI_API_KEY is required")
    return SpeechConfig(
        api_key=api_key,
        language_code=os.getenv("ASSEMBLYAI_LANGUAGE_CODE"),
        speaker_labels=os.getenv("ASSEMBLYAI_SPEAKER_LABELS", "false").lower() == "true",
        punctuate=os.getenv("ASSEMBLYAI_PUNCTUATE", "true").lower() != "false",
        format_text=os.getenv("ASSEMBLYAI_FORMAT_TEXT", "true").lower() != "false",
    )


def create_client(config: Optional[SpeechConfig] = None) -> aai.Transcriber:
    cfg = config or load_config()
    aai.settings.api_key = cfg.api_key
    return aai.Transcriber()


def normalize_audio_source(audio_source: str) -> str:
    if audio_source.startswith(("http://", "https://")):
        return audio_source
    return os.path.abspath(audio_source)
