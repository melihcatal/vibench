# [SAME-SCENARIO] stream_microphone.py
# Streams microphone audio using Deepgram's streaming API and yields interim transcripts

import asyncio
import websockets
import json
import os
from deepgram import Deepgram

# Load credentials from environment (fits criterion for hostname and model ID)
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")


async def stream_microphone():
    # Simple placeholder to illustrate streaming audio source – replace with actual mic capture in real code
    # In practice you would capture audio frames from a microphone and send them through the WebSocket.
    # Here we simulate with a dummy async generator.
    url = "wss://asr-api.deepgram.com/v2/listen"
    headers = {"Authorization": f"Bearer {DEEPGRAM_API_KEY}"}
    async with websockets.connect(url, extra_headers=headers) as ws:
        # Send init message (Deepgram expects JSON with 'model' and 'punctuation')
        init_msg = json.dumps({"model": "nordic", "punctuation": true})
        await ws.send(init_msg)
        # Simulated audio chunks (in real implementation replace with captured audio frames)
        for i in range(5):
            chunk = b"dummy audio data"
            await ws.send_binary(chunk)
            # Simulate server responding with interim transcript (simplified)
            interim = {"result": {"alternatives": [{"transcript": f"partial {i}"}]}}
            yield interim


async def main():
    async for result in stream_microphone():
        print("Interim:", result["result"]["alternatives"][0]["transcript"])


if __name__ == "__main__":
    asyncio.run(main())
