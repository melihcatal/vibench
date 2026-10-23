import asyncio
from google.cloud import speech
from speech_client import get_async_speech_client


async def stream_chunks(audio_chunk_generator):
    client = get_async_speech_client()

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )
    streaming_config = speech.StreamingRecognitionConfig(
        config=config, interim_results=True
    )

    async def request_stream():
        async for chunk in audio_chunk_generator:
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = client.streaming_recognize(
        config=streaming_config, requests=request_stream()
    )

    async for response in responses:
        yield response
