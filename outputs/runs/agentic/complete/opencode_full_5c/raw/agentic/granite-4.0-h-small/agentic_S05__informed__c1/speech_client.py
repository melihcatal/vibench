# [HELPER] speech_client.py
# Local configuration and client utilities for Streaming Speech-to-Text

import os
import asyncio
import websockets
import json

# Default credentials placeholders (replace with real env vars in production)
DEFAULT_DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
DEFAULT_AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
DEFAULT_AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Central client factory for speech services


async def create_deepgram_client(api_key: str = None):
    """Returns an async generator that streams audio to Deepgram and yields results."""
    key = api_key or DEFAULT_DEEPGRAM_API_KEY
    url = "wss://asr-api.deepgram.com/v2/listen"
    headers = {"Authorization": f"Bearer {key}"}
    async with websockets.connect(url, extra_headers=headers) as ws:
        init_msg = json.dumps({"model": "nordic", "punctuation": True})
        await ws.send(init_msg)
        # Yields each incoming JSON response as a dict
        while True:
            resp = await ws.recv()
            try:
                yield json.loads(resp)
            except json.JSONDecodeError:
                continue


# Example helper if you need a different service (e.g., AWS Transcribe) would plug in here


async def main():
    async for result in create_deepgram_client():
        print("Received Deepgram result:", result)


if __name__ == "__main__":
    asyncio.run(main())
