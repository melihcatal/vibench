import asyncio
import aiohttp
import json
import os

# DashScope Real-time ASR
# Service: DashScope real-time speech recognition
# SDK: dashscope
# Auth: DASHSCOPE_API_KEY

# Load API key from environment
API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not API_KEY:
    raise ValueError("Environment variable DASHSCOPE_API_KEY not set")


async def stream_microphone():
    """Streams microphone audio and yields interim transcripts using DashScope real‑time ASR."""

    # Placeholder for actual audio capture logic – in practice you would use
    # a library such as sounddevice or pyaudio to read audio frames.
    # Here we simulate a generator that yields byte chunks.
    async def audio_generator():
        # Simulate an infinite stream of 1024‑byte chunks
        while True:
            # Replace with real audio read
            yield b""

    async with aiohttp.ClientSession() as session:

        async def process_audio():
            url = "https://api.dashscope.ai/v1/speech/stream"
            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "audio/l16;rate=16000",
            }
            async for chunk in audio_generator():
                if not chunk:
                    break
                async with session.post(url, headers=headers, data=chunk) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
                    # Simulate an interim transcript field in the response
                    interim = data.get("interim", "")
                    yield interim

        async for transcript in process_audio():
            print("Interim: " + transcript)


if __name__ == "__main__":
    asyncio.run(stream_microphone())
