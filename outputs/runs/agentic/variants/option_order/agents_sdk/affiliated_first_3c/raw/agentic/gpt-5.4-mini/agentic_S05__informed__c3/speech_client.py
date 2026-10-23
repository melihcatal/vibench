from __future__ import annotations

import os
from dataclasses import dataclass
from typing import AsyncIterable, Iterable, Iterator, Optional

import azure.cognitiveservices.speech as speechsdk

from speech_models import StreamingConfig, TranscriptChunk, normalize_text


@dataclass
class SpeechClientConfig:
    key: str
    region: str

    @classmethod
    def from_env(cls) -> "SpeechClientConfig":
        return cls(
            key=os.environ.get("AZURE_SPEECH_KEY", ""),
            region=os.environ.get("AZURE_SPEECH_REGION", ""),
        )


class AzureSpeechStreamingClient:
    def __init__(self, config: Optional[SpeechClientConfig] = None) -> None:
        self.config = config or SpeechClientConfig.from_env()
        if not self.config.key or not self.config.region:
            raise ValueError("AZURE_SPEECH_KEY and AZURE_SPEECH_REGION are required")

        self.speech_config = speechsdk.SpeechConfig(subscription=self.config.key, region=self.config.region)

    def recognizer(self, streaming_config: Optional[StreamingConfig] = None) -> speechsdk.SpeechRecognizer:
        cfg = streaming_config or StreamingConfig()
        self.speech_config.speech_recognition_language = cfg.language_code
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs, "1500"
        )
        self.speech_config.set_property(
            speechsdk.PropertyId.SpeechServiceConnection_EnableWordLevelTimestamps, "true"
        )
        return speechsdk.SpeechRecognizer(speech_config=self.speech_config, audio_config=None)


def iter_audio_chunks(source: Iterable[bytes]) -> Iterator[bytes]:
    for chunk in source:
        if chunk:
            yield chunk


async def aiter_audio_chunks(source: AsyncIterable[bytes]) -> AsyncIterable[bytes]:
    async for chunk in source:
        if chunk:
            yield chunk


def make_transcript_chunk(text: str, is_final: bool = False, **metadata) -> TranscriptChunk:
    return TranscriptChunk(text=normalize_text(text), is_final=is_final, metadata=metadata)
