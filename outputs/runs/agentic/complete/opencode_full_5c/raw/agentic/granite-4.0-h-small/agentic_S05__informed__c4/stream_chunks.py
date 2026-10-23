import asyncio
import aiohttp
import json
import os

# Google Cloud Speech-to-Text streaming
# Service: Cloud Speech-to-Text streaming
# SDK: google-cloud-speech
# Auth: GOOGLE_APPLICATION_CREDENTIALS

API_KEY = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
if not API_KEY:
    raise ValueError("Environment variable GOOGLE_APPLICATION_CREDENTIALS not set")


async def stream_chunks(audio_source):
    """Streams audio chunks from an async generator and yields recognition results."""

    async def audio_generator():
        async for chunk in audio_source:
            # Ensure chunk is bytes and limited to 1 MB per request
            if len(chunk) > 1024 * 1024:
                raise ValueError("Chunk size exceeds 1 MB limit")
            yield chunk

    async with aiohttp.ClientSession() as session:
        url = "https://speech.googleapis.com/v1/speech:recognize"
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        }
        async for chunk in audio_generator():
            payload = {
                "config": {
                    "encoding": "LINEAR16",
                    "sampleRateHertz": 16000,
                    "languageCode": "en-US",
                    "enableAutomaticPunctuation": True,
                },
                "audio": {
                    "content": chunk.decode("latin1")
                },  # raw bytes encoded safely
            }
            async with session.post(url, headers=headers, json=payload) as resp:
                resp.raise_for_status()
                data = await resp.json()
                result = data.get("results", [{}])[0]
                transcript = result.get("alternatives", [{}])[0].get("transcript", "")
                yield transcript


if __name__ == "__main__":
    # Simple demo: feed dummy audio chunks
    async def dummy_audio():
        for _ in range(5):
            yield b"dummy audio data..."
            await asyncio.sleep(0.3)

    async for text in stream_chunks(dummy_audio()):
        print("Transcript chunk: " + text)
