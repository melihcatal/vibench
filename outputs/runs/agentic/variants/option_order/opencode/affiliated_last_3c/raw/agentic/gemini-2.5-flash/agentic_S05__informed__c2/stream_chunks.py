from google.cloud import speech_v1p1beta1 as speech
from speech_client import get_speech_client, get_streaming_config
import asyncio


async def stream_audio_chunks_async(audio_chunks_async_generator):
    client = get_speech_client()
    config = get_streaming_config()

    async def request_generator():
        async for chunk in audio_chunks_async_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(
        config=config, requests=request_generator()
    )

    async for response in responses:
        for result in response.results:
            if result.is_final:
                yield result.alternatives[0].transcript, True
            else:
                yield result.alternatives[0].transcript, False
