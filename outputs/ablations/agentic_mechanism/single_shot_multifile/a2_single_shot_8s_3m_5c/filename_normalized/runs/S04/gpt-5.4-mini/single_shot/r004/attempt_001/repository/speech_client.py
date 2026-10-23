from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Optional

import assemblyai as aai

from speech_models import AudioSource


@dataclass
class SpeechClientConfig:
    api_key: str
    default_model: Optional[str] = None
    timeout_seconds: int = 120


def load_config() -> SpeechClientConfig:
    api_key = os.getenv('ASSEMBLYAI_API_KEY', '')
    if not api_key:
        raise RuntimeError('ASSEMBLYAI_API_KEY is required')
    return SpeechClientConfig(api_key=api_key, default_model=os.getenv('ASSEMBLYAI_MODEL'), timeout_seconds=int(os.getenv('SPEECH_TIMEOUT_SECONDS', '120')))


def get_client() -> Any:
    cfg = load_config()
    aai.settings.api_key = cfg.api_key
    return aai


def resolve_audio_input(audio_path: str) -> AudioSource:
    path = Path(audio_path)
    if audio_path.startswith('http://') or audio_path.startswith('https://'):
        return AudioSource(url=audio_path)
    if not path.exists():
        raise FileNotFoundError(audio_path)
    return AudioSource(file_path=str(path))
