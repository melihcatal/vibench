# [SAME-SCENARIO] stream_chunks.py
# Streams audio chunks from an async iterator and sends them to Deepgram streaming API for transcription

import asyncio
import json
import websockets
import os
from deepgram import Deepgram

# Deepgram credentials (fits hostname and model identifier requirements)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


async def stream_chunks(source_async_iterator):
    """
    source_async_iterator: an async generator yielding bytes (audio chunks)
    Yields interim and final recognition results from Deepgram.
    """
    url = "wss://asr-api.deepgram.com/v2/listen"
    headers = {"Authorization": f"Bearer {DEEPGRAM_API_KEY}"}
    async with websockets.connect(url, extra_headers=headers) as ws:
        init_msg = json.dumps({"model": "nordic", "punctuation": True})
        await ws.send(init_msg)
        async for chunk in source_async_iterator:
            if not chunk:
                break
            await ws.send_binary(chunk)

        # Keep reading responses until the connection closes
        while True:
            response = await ws.recv()
            try:
                data = json.loads(response)
                if "result" in data:
                    yield data  # Final result or interim result containing transcript
            except json.JSONDecodeError:
                continue


async def source_generator():
    # Dummy async generator that yields small byte chunks for demonstration
    for i in range(3):
        yield b"dummy audio chunk " + str(i).encode()
        await asyncio.sleep(0.5)


async def main():
    async for result in stream_chunks(source_generator()):
        print("Received:", result)


if __name__ == "__main__":
    asyncio.run(main())
