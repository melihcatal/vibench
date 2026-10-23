import asyncio
import os
from typing import AsyncIterator, Optional

from google.cloud.speech_v1p1beta1 import SpeechClient
from google.cloud.speech_v1p1beta1.types import RecognitionConfig, StreamingRecognitionConfig, StreamingRecognizeRequest

from speech_client import get_speech_client, get_streaming_config
from speech_models import AudioChunk

async def stream_with_language_and_punctuation(
    async_audio_source: AsyncIterator[AudioChunk],
    language_code: str = "en-US",
    enable_automatic_punctuation: bool = True,
    model: str = "default",
    profanity_filter: bool = False,
    enable_word_time_offsets: bool = False
) -> AsyncIterator[StreamingRecognizeRequest]:
    client: SpeechClient = get_speech_client()

    first_chunk = None
    try:
        first_chunk = await async_audio_source.__anext__()
    except StopAsyncIteration:
        pass

    sample_rate_hertz = first_chunk.sample_rate_hertz if first_chunk else 16000

    config = get_streaming_config(
        language_code=language_code,
        enable_automatic_punctuation=enable_automatic_punctuation,
        model=model,
        profanity_filter=profanity_filter,
        enable_word_time_offsets=enable_word_time_offsets,
        sample_rate_hertz=sample_rate_hertz
    )
    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    yield StreamingRecognizeRequest(streaming_config=streaming_config)

    if first_chunk:
        yield StreamingRecognizeRequest(audio_content=first_chunk.content)

    async for chunk in async_audio_source:
        yield StreamingRecognizeRequest(audio_content=chunk.content)
