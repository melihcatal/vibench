from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import dashscope
from dashscope.audio.asr import Recognition, RecognitionCallback

from speech_models import NormalizedTranscriptEvent, SpeechChunk

DEFAULT_MODEL = "paraformer-realtime-v1"


@dataclass(frozen=True)
class SpeechClientConfig:
    api_key: str
    model: str = DEFAULT_MODEL
    sample_rate: int = 16000
    format: str = "pcm"
    language: Optional[str] = None
    punctuation: bool = True

    @classmethod
    def from_env(cls) -> "SpeechClientConfig":
        return cls(
            api_key=os.getenv("DASHSCOPE_API_KEY", ""),
            model=os.getenv("DASHSCOPE_ASR_MODEL", DEFAULT_MODEL),
            sample_rate=int(os.getenv("DASHSCOPE_SAMPLE_RATE", "16000")),
            format=os.getenv("DASHSCOPE_AUDIO_FORMAT", "pcm"),
            language=os.getenv("DASHSCOPE_ASR_LANGUAGE"),
            punctuation=os.getenv("DASHSCOPE_ASR_PUNCTUATION", "true").lower() == "true",
        )


class SpeechStreamCallback(RecognitionCallback):
    def __init__(self) -> None:
        self.events: list[NormalizedTranscriptEvent] = []

    def on_open(self) -> None:
        return None

    def on_event(self, result: Dict[str, Any]) -> None:
        self.events.append(NormalizedTranscriptEvent.from_dashscope(result))

    def on_error(self, error: Exception) -> None:
        self.events.append(NormalizedTranscriptEvent(text=str(error), is_final=True, stability=0.0))

    def on_close(self) -> None:
        return None


class StreamingSpeechClient:
    def __init__(self, config: Optional[SpeechClientConfig] = None) -> None:
        self.config = config or SpeechClientConfig.from_env()
        if self.config.api_key:
            dashscope.api_key = self.config.api_key

    def start_recognizer(self, callback: Optional[SpeechStreamCallback] = None, **kwargs: Any) -> Recognition:
        cb = callback or SpeechStreamCallback()
        params: Dict[str, Any] = {
            "model": self.config.model,
            "format": self.config.format,
            "sample_rate": self.config.sample_rate,
            "callback": cb,
        }
        if self.config.language:
            params["language"] = self.config.language
        if self.config.punctuation:
            params["enable_punctuation"] = True
        params.update(kwargs)
        return Recognition(**params)

    def chunk_to_audio_payload(self, chunk: SpeechChunk) -> bytes:
        return chunk.audio
