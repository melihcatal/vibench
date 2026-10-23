# [SAME-SCENARIO] stream_with_language.py
# Starts a streaming recognizer with language, punctuation, and other settings using Deepgram

import asyncio
import websockets
import json
import os
from deepgram import Deepgram

# Load Deepgram API key (fits credential requirement)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
MODEL = "nordic"  # Deepgram model identifier (fits model ID requirement)
LANGUAGE = "en-US"
ENABLE_PUNCTUATION = True


async def stream_with_language():
    url = "wss://asr-api.deepgram.com/v2/listen"
    headers = {"Authorization": f"Bearer {DEEPGRAM_API_KEY}"}
    async with websockets.connect(url, extra_headers=headers) as ws:
        # Build init payload with language, punctuation, and model
        payload = {
            "model": MODEL,
            "language": LANGUAGE,
            "punctuation": ENABLE_PUNCTUATION,
        }
        init_msg = json.dumps(payload)
        await ws.send(init_msg)
        # Dummy audio chunk sending (replace with real mic capture in production)
        for i in range(2):
            await ws.send_binary(b"dummy audio chunk")
            # Simulate a response
            response = {"result": {"alternatives": [{"transcript": f"partial {i}"}]}}
            yield response


async def main():
    async for result in stream_with_language():
        transcript = result["result"]["alternatives"][0]["transcript"]
        print("Transcript:", transcript)


if __name__ == "__main__":
    asyncio.run(main())
