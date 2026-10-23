from typing import AsyncIterable, AsyncIterator

from google.cloud import speech

from speech_client import (
    build_speech_client,
    build_streaming_config,
    load_stream_config,
)


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = build_speech_client()
    config = build_streaming_config(load_stream_config())

    async def requests():
        async for chunk in source:
            if chunk:
                yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(config=config, requests=requests())
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
