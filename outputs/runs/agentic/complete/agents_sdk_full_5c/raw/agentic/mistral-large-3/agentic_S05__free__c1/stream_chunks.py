import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_results

async def stream_chunks(audio_chunk_source):
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "config": {
                "encoding": "LINEAR16",
                "sample_rate_hertz": 16000,
                "language_code": "en-US",
                "model": "latest_long",
            }
        }
    )

    async def chunk_generator():
        async for chunk in audio_chunk_source:
            yield chunk

    await stream.write(chunk_generator())
    async for response in stream:
        await handle_partial_results(response)