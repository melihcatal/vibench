import os
from typing import Any, AsyncIterable, Iterable, Optional

from deepgram import DeepgramClient, LiveOptions

from speech_models import SpeechStreamConfig


def get_deepgram_client() -> DeepgramClient:
    api_key = os.environ["DEEPGRAM_API_KEY"]
    return DeepgramClient(api_key)


def build_live_options(config: Optional[SpeechStreamConfig] = None) -> LiveOptions:
    config = config or SpeechStreamConfig()
    return LiveOptions(
        model=config.model,
        language=config.language_code,
        punctuate=config.punctuation,
        interim_results=config.interim_results,
    )


async def stream_source(
    source: AsyncIterable[bytes] | Iterable[bytes], sink: Any
) -> None:
    if hasattr(source, "__aiter__"):
        async for chunk in source:
            await sink.send(chunk)
    else:
        for chunk in source:
            await sink.send(chunk)
