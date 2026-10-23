from typing import AsyncIterator, Iterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import build_client, load_config, streaming_config


async def stream_chunks(source: AsyncIterator[bytes]) -> Iterator[str]:
    client = build_client()
    config = load_config()

    async def request_iter():
        async for chunk in source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(streaming_config(config), request_iter())
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
