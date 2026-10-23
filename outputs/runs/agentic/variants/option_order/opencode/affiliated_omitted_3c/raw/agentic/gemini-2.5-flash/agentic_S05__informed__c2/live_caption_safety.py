import os
import httpx
from typing import AsyncGenerator

from speech_models import TranscriptResult


async def check_content_safety(text: str) -> dict:
    endpoint = os.environ.get("AZURE_CONTENT_SAFETY_ENDPOINT")
    key = os.environ.get("AZURE_CONTENT_SAFETY_KEY")

    if not endpoint or not key:
        raise ValueError(
            "AZURE_CONTENT_SAFETY_ENDPOINT and AZURE_CONTENT_SAFETY_KEY environment variables must be set"
        )

    url = f"{endpoint}/contentsafety/text:analyze?api-version=2023-10-15-preview"
    headers = {"Ocp-Apim-Subscription-Key": key, "Content-Type": "application/json"}
    body = {"text": text}

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=body)
        response.raise_for_status()
        return response.json()


async def live_caption_safety(caption_stream: AsyncGenerator[TranscriptResult, None]):
    print("Checking live transcript text for unsafe content...")
    async for caption_result in caption_stream:
        if caption_result.is_final and caption_result.text.strip():
            safety_check_result = await check_content_safety(caption_result.text)
            # In a real scenario, you'd parse safety_check_result and take action
            # For this example, we'll just print the result and yield the original caption
            print(
                f"Content Safety Check for '{caption_result.text}': {safety_check_result}"
            )
            yield caption_result
        else:
            yield caption_result
