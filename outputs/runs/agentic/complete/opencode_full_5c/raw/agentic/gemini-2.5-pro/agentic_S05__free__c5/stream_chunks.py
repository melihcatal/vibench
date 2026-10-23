import asyncio
from google.cloud import speech
from speech_client import get_speech_client, get_streaming_config


async def stream_chunks(audio_chunk_generator):
    client = get_speech_client()
    streaming_config = speech.StreamingRecognitionConfig(
        config=get_streaming_config(),
        interim_results=True,
    )

    async def request_generator():
        async for chunk in audio_chunk_generator():
            yield speech.StreamingRecognizeRequest(audio_content=chunk)

    responses = await client.streaming_recognize(streaming_config, request_generator())

    async for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
