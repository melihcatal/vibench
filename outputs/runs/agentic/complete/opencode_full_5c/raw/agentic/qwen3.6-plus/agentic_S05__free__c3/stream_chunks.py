import asyncio
from typing import AsyncIterator, AsyncIterable
from google.cloud import speech_v1p1beta1 as speech
from google.api_core.exceptions import GoogleAPIClientError


async def stream_audio_chunks(
    audio_source: AsyncIterable[bytes],
    sample_rate: int = 16000,
    language_code: str = "en-US",
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
    interim_results: bool = True,
    chunk_size: int = 4096,
) -> AsyncIterator[dict]:
    from google.cloud.speech_v1p1beta1.services.speech.async_client import (
        SpeechAsyncClient,
    )

    client = SpeechAsyncClient()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=sample_rate,
        language_code=language_code,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
    )

    streaming_config = speech.StreamingRecognitionConfig(
        config=config,
        interim_results=interim_results,
    )

    async def request_generator():
        yield speech.StreamingRecognizeRequest(streaming_config=streaming_config)
        async for audio_data in audio_source:
            if len(audio_data) > chunk_size:
                for i in range(0, len(audio_data), chunk_size):
                    chunk = audio_data[i : i + chunk_size]
                    yield speech.StreamingRecognizeRequest(audio_content=chunk)
            else:
                yield speech.StreamingRecognizeRequest(audio_content=audio_data)

    responses = await client.streaming_recognize(requests=request_generator())

    async for response in responses:
        for result in response.results:
            transcript = (
                result.alternatives[0].transcript if result.alternatives else ""
            )
            is_final = result.is_final
            confidence = (
                result.alternatives[0].confidence if result.alternatives else 0.0
            )
            yield {
                "transcript": transcript,
                "is_final": is_final,
                "confidence": confidence,
                "stability": result.stability,
                "result_end_time": result.result_end_time.total_seconds()
                if result.result_end_time
                else 0.0,
                "language_code": language_code,
            }


async def stream_from_buffer(
    buffer: asyncio.Queue,
    sample_rate: int = 16000,
    language_code: str = "en-US",
    model: str = "latest_long",
    enable_automatic_punctuation: bool = True,
    interim_results: bool = True,
) -> AsyncIterator[dict]:
    async def audio_source():
        while True:
            chunk = await buffer.get()
            if chunk is None:
                break
            yield chunk

    async for result in stream_audio_chunks(
        audio_source=audio_source(),
        sample_rate=sample_rate,
        language_code=language_code,
        model=model,
        enable_automatic_punctuation=enable_automatic_punctuation,
        interim_results=interim_results,
    ):
        yield result
