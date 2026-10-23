from __future__ import annotations

from typing import AsyncIterable, AsyncIterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_client, build_streaming_config, chunk_audio_stream
from speech_models import SpeechStreamConfig


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = build_client()
    config = SpeechStreamConfig(language_code="en-US", punctuation=True, interim_results=True)
    requests = chunk_audio_stream(source)
    responses = client.streaming_recognize(build_streaming_config(config), requests)
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
