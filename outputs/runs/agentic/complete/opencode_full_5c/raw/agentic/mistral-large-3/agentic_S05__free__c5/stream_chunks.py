import asyncio
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types
from speech_client import get_speech_client
from speech_models import StreamingRecognitionConfig


async def stream_chunks(audio_chunk_queue):
    client = get_speech_client()
    config = StreamingRecognitionConfig(
        config=types.RecognitionConfig(
            encoding=types.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
            model="latest_long",
        ),
        interim_results=True,
    )

    async def request_generator():
        while True:
            chunk = await audio_chunk_queue.get()
            if chunk is None:
                break
            yield types.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(config, request_generator())

    async for response in responses:
        for result in response.results:
            yield {
                "transcript": result.alternatives[0].transcript,
                "is_final": result.is_final,
                "stability": result.stability,
            }
