# SAME-SCENARIO: stream_chunks.py
# streams audio chunks from an async source
import asyncio
import aiohttp  # pip install aiohttp
import deepgram  # pip install deepgram-sdk-python

# Deepgram Streaming SDK imported – provider identifiable
DEEPGRAM_API_KEY = "YOUR_DEEPGRAM_API_KEY"


async def stream_chunks(source_url: str):
    """Stream pre-recorded audio chunks to Deepgram and print partial results.

    Args:
        source_url: HTTP URL of the audio file to stream (e.g., an MP3).
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(source_url) as resp:
            resp.raise_for_status()
            # Chunk size of ~1024 bytes (adjust as needed)
            chunk_size = 1024
            async for chunk in resp.content.iter_chunked(chunk_size):
                # Deepgram accepts raw 16‑bit PCM data; assume source provides it or convert as needed
                await ws.send_bytes(chunk)

        # After streaming all chunks, wait for final result
        response = await ws.receive_json()
        for result in response.get("results", []):
            print(
                "Final transcript:",
                result.get("alternatives", [{}])[0].get("transcript"),
            )


async def start_stream_chunks():
    source = "https://example.com/audio_sample.wav"
    connector = aiohttp.TCPConnector(limit=1)
    async with deepgram.Stream(
        "wss://api.deepgram.io/v1/stream", DEEPGRAM_API_KEY, connector=connector
    ) as ws:
        await stream_chunks(source)


if __name__ == "__main__":
    asyncio.run(start_stream_chunks())
