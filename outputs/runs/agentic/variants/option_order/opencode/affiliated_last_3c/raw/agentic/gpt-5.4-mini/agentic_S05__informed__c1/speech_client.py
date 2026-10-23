import os
from dataclasses import dataclass
from typing import Any, AsyncIterator, Awaitable, Callable, Iterable, Optional

from deepgram import DeepgramClient, DeepgramClientOptions, LiveOptions


@dataclass
class SpeechConfig:
    api_key: str
    model: str = "nova-2"
    language: Optional[str] = None
    punctuate: bool = True


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ["DEEPGRAM_API_KEY"],
        model=os.getenv("DEEPGRAM_MODEL", "nova-2"),
        language=os.getenv("DEEPGRAM_LANGUAGE"),
        punctuate=os.getenv("DEEPGRAM_PUNCTUATE", "true").lower() != "false",
    )


def create_deepgram_client(config: Optional[SpeechConfig] = None) -> DeepgramClient:
    config = config or load_speech_config()
    return DeepgramClient(
        config.api_key, config=DeepgramClientOptions(options={"keepalive": "true"})
    )


def build_live_options(config: Optional[SpeechConfig] = None) -> LiveOptions:
    config = config or load_speech_config()
    options = {
        "model": config.model,
        "punctuate": config.punctuate,
        "interim_results": True,
    }
    if config.language:
        options["language"] = config.language
    return LiveOptions(**options)


async def iter_bytes(source: Any) -> AsyncIterator[bytes]:
    if hasattr(source, "__aiter__"):
        async for item in source:
            yield item
    else:
        for item in source:
            yield item
