import asyncio
import os
from typing import AsyncIterator

from google.cloud.speech_v1p1beta1 import SpeechClient
from google.cloud.speech_v1p1beta1.types import RecognitionConfig, StreamingRecognitionConfig, StreamingRecognizeRequest

from speech_client import get_speech_client, get_streaming_config
from speech_models import AudioChunk, TranscriptResult

async def stream_chunks_from_async_source(async_audio_source: AsyncIterator[AudioChunk]) -> AsyncIterator[StreamingRecognizeRequest]:
    client: SpeechClient = get_speech_client()

    # Assume a default config, can be overridden if needed
    # Extract sample_rate_hertz from the first chunk if available, otherwise default
    first_chunk = None
    try:
        first_chunk = await async_audio_source.__anext__()
    except StopAsyncIteration:
        pass

    sample_rate_hertz = first_chunk.sample_rate_hertz if first_chunk else 16000

    config = get_streaming_config(language_code="en-US", enable_automatic_punctuation=True, sample_rate_hertz=sample_rate_hertz)
    streaming_config = StreamingRecognitionConfig(config=config, interim_results=True)

    yield StreamingRecognizeRequest(streaming_config=streaming_config)

    if first_chunk:
        yield StreamingRecognizeRequest(audio_content=first_chunk.content)

    async for chunk in async_audio_source:
        yield StreamingRecognizeRequest(audio_content=chunk.content)
