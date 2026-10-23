from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

from deepgram import DeepgramClient

from speech_models import TranscriptEvent, TranscriptChunk, normalize_text


@dataclass
class SpeechConfig:
    api_key: str
    model: str = "nova-3"
    language: Optional[str] = None
    punctuate: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        model=os.getenv("DEEPGRAM_MODEL", "nova-3"),
        language=os.getenv("DEEPGRAM_LANGUAGE"),
        punctuate=os.getenv("DEEPGRAM_PUNCTUATE", "true").lower() == "true",
    )


class DeepgramSpeechClient:
    def __init__(self, config: Optional[SpeechConfig] = None) -> None:
        self.config = config or load_speech_config()
        self.client = DeepgramClient(self.config.api_key)

    def _options(self) -> dict:
        options = {
            "model": self.config.model,
            "punctuate": self.config.punctuate,
            "interim_results": True,
            "smart_format": True,
        }
        if self.config.language:
            options["language"] = self.config.language
        return options

    def process_event(self, payload: dict) -> TranscriptEvent:
        channel = payload.get("channel", {})
        alternatives = channel.get("alternatives") or []
        transcript = normalize_text(alternatives[0].get("transcript", "")) if alternatives else ""
        return TranscriptEvent(
            text=transcript,
            is_final=bool(channel.get("is_final") or payload.get("is_final")),
            confidence=(alternatives[0].get("confidence") if alternatives else None),
            language_code=self.config.language,
            raw=payload,
        )
