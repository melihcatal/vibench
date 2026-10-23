# [LATER-STEP] live_caption_safety.py
# Perform unsafe content detection on live transcript fragments using Azure AI Content Safety (REST)
import asyncio
import aiohttp
import json

# Provider identifier
PROVIDER = "azure_content_safety"

# Azure environment variables (set before running)
CONTENT_SAFETY_ENDPOINT = "${AZURE_CONTENT_SAFETY_ENDPOINT}"  # e.g. https://<region>.api.cognitive.microsoft.com
CONTENT_SAFETY_KEY = "${AZURE_CONTENT_SAFETY_KEY}"

async def is_safe(text: str) -> bool:
    """Send text to Azure Content Safety API and return True if safe."""
    url = f"{CONTENT_SAFETY_ENDPOINT}/contentSafety/v1.0/moderate/text"
    headers = {
        "Ocp-Apim-Subscription-Key": CONTENT_SAFETY_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "content": text,
        "content_type": "text",
        "domain": "social",
        "category": "text"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as resp:
            resp.raise_for_status()
            result = await resp.json()
            # Assume safe if classification is not flagged as harmful
            categories = result.get("categories")
            flagged = categories.get("hate", {}).get("flagged", False) or \
                     categories.get("self_harm", {}).get("flagged", False) or \
                     categories.get("sexual", {}).get("flagged", False) or \
                     categories.get("violence", {}).get("flagged", False)
            return not flagged

async def safety_monitor(source: asyncio.Queue):
    """Consume live captions and print whether they are safe."""
    async for caption in source:
        safe = await is_safe(caption)
        print(f"[SAFE: {'YES' if safe else 'NO'}] {caption[:30]}{'...' if len(caption)>30 else ''}")

if __name__ == "__main__":
    # Demo using a simple queue of captions
    q = asyncio.Queue()
    async def producer():
        texts = [
            "I love open source software.",
            "You are an idiot."
        ]
        for t in texts:
            await q.put(t)
            await asyncio.sleep(1.0)
    producer_task = asyncio.create_task(producer())
    safety_task = asyncio.create_task(safety_monitor(q.get()))
    await asyncio.sleep(3.0)
    producer_task.cancel()
    try:
        await producer_task
    except asyncio.CancelledError:
        pass