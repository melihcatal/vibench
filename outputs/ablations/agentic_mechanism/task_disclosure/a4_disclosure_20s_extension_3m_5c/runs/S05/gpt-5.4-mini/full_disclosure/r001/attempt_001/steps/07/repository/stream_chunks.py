import asyncio
from typing import AsyncIterable, AsyncIterator, Optional

import google.cloud.speech_v1 as speech


async def stream_chunks(chunks: AsyncIterable[bytes], sample_rate_hertz: int = 16000, language_code: str = "en-US") -> AsyncIterator[str]:
    client = speech.SpeechAsyncClient()
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate_hertz,
        language_code=language_code,
        enable_automatic_punctuation=True,
    )
    streaming_config = speech.StreamingRecognitionConfig(config=config, interim_results=True)
    requests = _request_stream(chunks)
    responses = await client.streaming_recognize(streaming_config=streaming_config, requests=requests)
    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript


async def _request_stream(chunks: AsyncIterable[bytes]) -> AsyncIterator[speech.StreamingRecognizeRequest]:
    async for chunk in chunks:
        if chunk:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)
