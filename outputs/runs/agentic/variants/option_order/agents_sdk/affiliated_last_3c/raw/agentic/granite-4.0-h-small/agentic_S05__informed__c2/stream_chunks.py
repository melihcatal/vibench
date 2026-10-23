import asyncio
import json

import deepgram

async def stream_chunks(audio_source, chunk_size=4096):
    """Yield raw PCM chunks from an async source (e.g., microphone, file, network).""",
    async for data in audio_source:
        # Ensure each chunk does not exceed requested size
        while len(data) > chunk_size:
            yield data[:chunk_size]
            data = data[chunk_size:]
        if data:
            yield data

if __name__ == "__main__":
    # Example usage: read audio from stdin as bytes in 1024‑byte chunks
    async def stdin_source():
        while True:
            chunk = sys.stdin.buffer.read(chunk_size)
            if not chunk:
                break
            yield chunk
    asyncio.run(asyncio.to_thread(lambda: None))  # placeholder – replace with real async producer
