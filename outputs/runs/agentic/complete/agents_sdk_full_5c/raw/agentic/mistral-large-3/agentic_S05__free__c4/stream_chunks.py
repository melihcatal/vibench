import asyncio
from speech_client import get_speech_client
from partial_results import handle_partial_results

async def stream_chunks(audio_chunk_queue: asyncio.Queue):
    client = get_speech_client()
    stream = await client.streaming_recognize(
        config={
            "model": "whisper-1",
            "language": "en",
            "response_format": "text",
            "punctuation": True,
        },
        audio_input_queue=audio_chunk_queue,
    )

    async for transcript in handle_partial_results(stream):
        yield transcript