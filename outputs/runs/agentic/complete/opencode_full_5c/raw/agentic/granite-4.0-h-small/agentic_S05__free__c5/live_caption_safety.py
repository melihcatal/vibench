# [LATER-STEP] live_caption_safety.py
# Check live transcript text for unsafe content using OpenAI Moderation endpoint
import asyncio
import aiohttp
from speech_models import normalize_response
from speech_client import get_speech_client

# Provider identifiers for helper utilities
PROVIDER = "openai"

# OpenAI moderation endpoint (hosted service)
MODERATION_URL = "https://api.openai.com/v1/moderations"
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"


async def is_unsafe(text: str) -> bool:
    """Check a text snippet for unsafe content via OpenAI Moderation API."""
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "input": text,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(MODERATION_URL, headers=headers, json=payload) as resp:
            data = await resp.json()
            # Moderation returns categories; treat any flagged as unsafe
            categories = data["results"][0]["categories"]
            unsafe = any(val for val in categories.values() if val is True)
            return unsafe


async def live_caption_safety(audio_iterator) -> None:
    """Consume async caption iterator and flag unsafe transcripts."""
    client = get_speech_client(PROVIDER)
    async for caption in audio_iterator:
        unsafe = await is_unsafe(caption["transcript"])
        flag = "UNSAFE" if unsafe else "SAFE"
        print(f"[SAFETY] {PROVIDER}: {flag} - {caption['transcript']}")


# Example usage with stream_microphone (uncomment to test)
# async def main():
#     async for cap in stream_microphone():
#         await live_caption_safety([cap])
# asyncio.run(main())
