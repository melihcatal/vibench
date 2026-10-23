import os
from dataclasses import dataclass
from typing import AsyncIterable, Iterable, Optional

from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions


@dataclass
class SpeechConfig:
    api_key: str
    language: str = "en-US"
    punctuate: bool = True
    model: str = "nova-2"


def load_config(language: Optional[str] = None, punctuate: bool = True) -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        language=language or os.getenv("SPEECH_LANGUAGE", "en-US"),
        punctuate=punctuate,
        model=os.getenv("DEEPGRAM_MODEL", "nova-2"),
    )


def create_client(config: Optional[SpeechConfig] = None) -> DeepgramClient:
    cfg = config or load_config()
    return DeepgramClient(cfg.api_key)


def live_options(config: SpeechConfig, interim_results: bool = True) -> LiveOptions:
    return LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=interim_results,
        smart_format=True,
    )


async def stream_bytes(source: AsyncIterable[bytes], sink) -> None:
    async for chunk in source:
        if chunk:
            await sink.send(chunk)


def send_chunks(source: Iterable[bytes], sink) -> None:
    for chunk in source:
        if chunk:
            sink.send(chunk)
