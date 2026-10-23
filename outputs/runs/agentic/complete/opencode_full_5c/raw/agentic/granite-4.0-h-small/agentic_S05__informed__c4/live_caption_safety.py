import asyncio
import aiohttp
import json
from speech_client import SpeechClient
from speech_models import SpeechModels

# Tisane Text Moderation (service=Tisane Text Moderation)
# SDK: requests
# Auth: TISANE_API_KEY

TISANE_API_KEY = os.getenv("TISANE_API_KEY")
if not TISANE_API_KEY:
    raise ValueError("Environment variable TISANE_API_KEY not set")


async def safe_live_caption():
    """
    Streams captions via SpeechClient (e.g., Google) and filters each caption for unsafe content.
    Yields (caption, safe) tuples.
    """
    client = SpeechClient("google")
    async for chunk in client.stream_microphone():
        caption = client._normalize_response(chunk)
        if not caption:
            continue
        async with aiohttp.ClientSession() as session:
            url = "https://api.tisane.ai/v0/parse"
            headers = {
                "Authorization": f"Bearer {TISANE_API_KEY}",
                "Content-Type": "application/json",
            }
            payload = {"text": caption, "settings": {"languages": ["en"]}}
            async with session.post(url, headers=headers, json=payload) as resp:
                resp.raise_for_status()
                data = await resp.json()
                # Tisane returns a field like `moderation` with flags; simplify to a boolean
                safe = not data.get("moderation", {}).get("unsafe", False)
        yield caption, safe


if __name__ == "__main__":

    async def demo():
        async for caption, safe in safe_live_caption():
            print(f"Caption: {caption} ({'SAFE' if safe else 'UNSAFE'})")
            await asyncio.sleep(0.5)

    asyncio.run(demo())
