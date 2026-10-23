import asyncio
from typing import AsyncIterable

import deepgram

# Deepgram Streaming API credentials (environment variable)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


async def stream_chunks(source: AsyncIterable[bytes]) -> AsyncIterable[str]:
    """Streams audio chunks from an async iterable and yields interim transcripts from Deepgram."""
    client = deepgram.clients.StreamingClient(DEEPGRAM_API_KEY)
    # start connection; expects bytes (16kHz mono PCM)
    async with client.transcribe_stream(
        params={"model": "general", "punctuate": True}
    ) as stream:
        async for chunk in source:
            await stream.send(chunk)
            # receive interim results as they become available
            async for interim in stream.response.interim:
                yield interim.transcript

        # final result after stream ends
        final_result = await stream.response.result
        if final_result and final_result.results:
            yield final_result.results[0].alternatives[0].transcript


# Example usage with a local file async generator
# async for text in stream_chunks(read_audio_file_async("test.wav")):
#     print(text)
