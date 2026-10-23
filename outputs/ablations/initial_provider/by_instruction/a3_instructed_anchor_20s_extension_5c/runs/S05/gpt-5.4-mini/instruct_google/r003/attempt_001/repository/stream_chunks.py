from typing import AsyncIterable, AsyncIterator

from google.cloud import speech_v1p1beta1 as speech

from speech_client import create_speech_client, create_streaming_config
from speech_models import normalize_text


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterator[str]:
    client = create_speech_client()
    config = create_streaming_config()

    async def request_stream():
        async for chunk in source:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    for response in client.streaming_recognize(config=config, requests=request_stream()):
        for result in response.results:
            if result.alternatives:
                yield normalize_text(result.alternatives[0].transcript)
