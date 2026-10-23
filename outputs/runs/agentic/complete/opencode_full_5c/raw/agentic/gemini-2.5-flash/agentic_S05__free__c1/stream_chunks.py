import asyncio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import get_streaming_config


async def stream_audio_chunks(audio_chunks_async_generator, sampling_rate: int):
    client = speech.SpeechClient()
    streaming_config = get_streaming_config(sampling_rate)

    async def request_generator():
        yield speech.StreamingRecognizeRequest(audio_config=streaming_config)
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(request_generator())

    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
