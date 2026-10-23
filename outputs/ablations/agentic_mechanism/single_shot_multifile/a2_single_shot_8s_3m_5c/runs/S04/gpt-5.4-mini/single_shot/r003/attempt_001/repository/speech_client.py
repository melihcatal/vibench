from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import deepgram


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    base_url: Optional[str] = None
    default_model: str = "nova-2"
    default_language: Optional[str] = None


class SpeechClient:
    def __init__(self, config: SpeechConfig) -> None:
        options: Dict[str, Any] = {"api_key": config.api_key}
        if config.base_url:
            options["host"] = config.base_url
        self._client = deepgram.DeepgramClient(**options)
        self.transcriptions = self._client.listen.prerecorded.v("1")


def load_config() -> SpeechConfig:
    api_key = os.environ.get("DEEPGRAM_API_KEY", "")
    if not api_key:
        raise ValueError("DEEPGRAM_API_KEY is required")
    return SpeechConfig(api_key=api_key, base_url=os.environ.get("DEEPGRAM_API_URL"), default_model=os.environ.get("DEEPGRAM_MODEL", "nova-2"), default_language=os.environ.get("DEEPGRAM_LANGUAGE"))


def get_client(config: Optional[SpeechConfig] = None) -> SpeechClient:
    return SpeechClient(config or load_config())
