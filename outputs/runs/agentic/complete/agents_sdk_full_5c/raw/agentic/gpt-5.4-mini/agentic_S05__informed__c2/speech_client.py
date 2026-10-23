from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Iterable, Optional

from speech_models import StreamingUtterance, normalize_caption


@dataclass(frozen=True)
class SpeechConfig:
    api_key: str
    language: str = "en-US"
    punctuation: bool = True
    model: str = "nova-2"

    @classmethod
    def from_env(cls) -> "SpeechConfig":
        return cls(
            api_key=os.environ.get("DEEPGRAM_API_KEY", ""),
            language=os.environ.get("DEEPGRAM_LANGUAGE", "en-US"),
            punctuation=os.environ.get("DEEPGRAM_PUNCTUATION", "true").lower() not in {"0", "false", "no"},
            model=os.environ.get("DEEPGRAM_MODEL", "nova-2"),
        )


class DeepgramSpeechClient:
    def __init__(self, config: Optional[SpeechConfig] = None) -> None:
        self.config = config or SpeechConfig.from_env()
        from deepgram import DeepgramClient, LiveOptions  # provider-identifying import

        self._dg = DeepgramClient(self.config.api_key)
        self._live_options_cls = LiveOptions

    def live_options(self) -> Any:
        return self._live_options_cls(
            model=self.config.model,
            language=self.config.language,
            punctuate=self.config.punctuation,
            interim_results=True,
            smart_format=True,
        )

    def transcribe_event(self, event: Any) -> StreamingUtterance:
        channel = getattr(event, "channel", None)
        alt = None
        if channel is not None:
            alternatives = getattr(channel, "alternatives", None) or []
            if alternatives:
                alt = alternatives[0]
        text = normalize_caption(getattr(alt, "transcript", "") if alt else "")
        return StreamingUtterance(
            text=text,
            is_final=bool(getattr(event, "is_final", False)),
            confidence=float(getattr(alt, "confidence", 0.0) or 0.0) if alt else None,
        )

    def client(self) -> Any:
        return self._dg


def iter_audio_bytes(source: Iterable[bytes]) -> Iterable[bytes]:
    for chunk in source:
        if chunk:
            yield chunk
