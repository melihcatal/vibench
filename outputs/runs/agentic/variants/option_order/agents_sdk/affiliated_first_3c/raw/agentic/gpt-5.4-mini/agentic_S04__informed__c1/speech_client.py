from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

import assemblyai as aai


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str

    @classmethod
    def from_env(cls) -> "SpeechConfig":
        api_key = os.getenv("ASSEMBLYAI_API_KEY")
        if not api_key:
            raise EnvironmentError("ASSEMBLYAI_API_KEY is required")
        return cls(api_key=api_key)


class SpeechClientFactory:
    @staticmethod
    def create(config: Optional[SpeechConfig] = None) -> aai.Transcriber:
        cfg = config or SpeechConfig.from_env()
        aai.settings.api_key = cfg.api_key
        return aai.Transcriber()
