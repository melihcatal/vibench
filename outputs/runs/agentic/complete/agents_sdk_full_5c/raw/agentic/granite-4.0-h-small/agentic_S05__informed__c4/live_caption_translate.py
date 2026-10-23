# [LATER-STEP] live_caption_translate.py
# Translate live caption fragments into another language using DeepL API (REST)
import asyncio
import aiohttp
import json

# Provider identifier
PROVIDER = "deepl"

# Environment variables (set before running)
DEEPL_AUTH_KEY = "${DEEPL_AUTH_KEY}"
TARGET_LANG = "fr"  # example: French

async def translate_caption(text: str) -> str:
    """Translate a caption fragment using DeepL REST API."""
    url = "https://api.deepl.com/v2/translate"
    payload = {
        "auth_key": DEEPL_AUTH_KEY,
        "text": text,
        "target_lang": TARGET_LANG
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload) as resp:
            resp.raise_for_status()
            data = await resp.json()
            translated = data["translations"][0]["text"]
            return translated

async def live_translation(source: asyncio.Queue):
    """Consume caption fragments from an async queue and print translations."""
    async for caption in source:
        translated = await translate_caption(caption)
        print(f"[TRANSLATED] {translated}")

if __name__ == "__main__":
    # Demo: simulate live captions via an asyncio.Queue
    q = asyncio.Queue()
    async def producer():
        phrases = [
            "Hello everyone, welcome to the meeting.",
            "Let's begin the discussion."
        ]
        for p in phrases:
            await q.put(p)
            await asyncio.sleep(1.0)
    producer_task = asyncio.create_task(producer())
    translation_task = asyncio.create_task(live_translation(q.get()))
    # Wait a bit so translation has something to consume
    await asyncio.sleep(3.0)
    producer_task.cancel()
    try:
        await producer_task
    except asyncio.CancelledError:
        pass