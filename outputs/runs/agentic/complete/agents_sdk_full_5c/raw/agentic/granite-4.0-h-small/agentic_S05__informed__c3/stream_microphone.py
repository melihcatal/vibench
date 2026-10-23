import asyncio
import aiohttp
import json
from dotenv import load_dotenv
import speech_client as sc

load_dotenv()

async def stream_microphone():
    # Configure microphone audio capture (using pyaudio or similar)
    # Placeholder for actual audio capture logic
    async for audio_chunk in sc.capture_microphone_audio():
        # Send audio chunk to streaming service (e.g., Google Cloud Speech)
        response = await sc.send_streaming_request(audio_chunk)
        # Parse response using helper utilities
        yield sc.parse_partial_results(response)

if __name__ == "__main__":
    asyncio.run(asyncio.gather(stream_microphone()))
