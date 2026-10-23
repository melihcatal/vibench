from __future__ import annotations

from collections.abc import AsyncIterable, Iterable
from typing import AsyncIterator, Iterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import SpeechConfig, build_streaming_config, get_speech_client


async def async_audio_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = get_speech_client()
    config = build_streaming_config(SpeechConfig())

    async def request_iter() -> AsyncIterator[speech.StreamingRecognizeRequest]:
        async for chunk in source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(config=config, requests=request_iter())
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
