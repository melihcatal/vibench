# Azure Content Safety (service=Azure AI Content Safety; sdk=requests / azure-ai-contentsafety)
# AZURE_CONTENT_SAFETY_ENDPOINT, AZURE_CONTENT_SAFETY_KEY environment variables required

import os
import requests
import asyncio
from typing import AsyncIterable
from .speech_models import normalize_result

CONTENT_ENDPOINT = os.getenv("AZURE_CONTENT_SAFETY_ENDPOINT")
CONTENT_KEY = os.getenv("AZURE_CONTENT_SAFETY_KEY")


def safety_request(text: str) -> requests.Response:
    """Send text to Azure Content Safety API for moderation."""
    if not CONTENT_ENDPOINT or not CONTENT_KEY:
        raise RuntimeError("Missing content safety credentials")
    headers = {"api-key": CONTENT_KEY}
    payload = {"input": {"kind": "plainText", "text": text}}
    response = requests.post(
        CONTENT_ENDPOINT + "/moderation/text", json=payload, headers=headers
    )
    response.raise_for_status()
    return response


async def check_live_safety(transcript_stream: AsyncIterable[str]):
    """Iterate over live transcript chunks and filter unsafe content."""
    async for chunk in transcript_stream:
        resp = safety_request(chunk)
        result = resp.json()
        # Simplified check: flag if any flagged category exists
        flagged = any(
            item["category"] in ["Hate", "Harassment", "Sexual", "Violence"]
            for item in result.get("results", [])
        )
        if flagged:
            print("Unsafe content detected:", chunk)
        else:
            print("Safe content:", chunk)


# Example with a dummy async iterable
async def demo():
    samples = ["Great meeting!", "I hate this product", "Let us celebrate"]

    async def async_sample_gen():
        for s in samples:
            yield s
            await asyncio.sleep(0.2)

    await check_live_safety(async_sample_gen())


if __name__ == "__main__":
    asyncio.run(demo())
