# [LATER-STEP] live_caption_translate.py
# Translate live captions into another language using Azure Translator Text API
import asyncio
import aiohttp
from speech_models import normalize_response
from speech_client import get_speech_client

# Provider identifiers for helper utilities
PROVIDER = "azure"

# Azure credentials (should be set in env vars for production)
AZURE_LOCATION = "eastus"
AZURE_TRANSLATOR_ENDPOINT = "https://api.cognitive.microsofttranslator.com/translate"
AZURE_TRANSLATOR_KEY = "YOUR_AZURE_TRANSLATOR_KEY"
TARGET_LANG = "es"  # Example: Spanish, change as needed


async def translate_text(text: str) -> str:
    """Translate a single text string using Azure Translator Text API."""
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_LOCATION,
        "Content-Type": "application/json",
    }
    body = [{"Text": text}]
    async with aiohttp.ClientSession() as session:
        async with session.post(
            AZURE_TRANSLATOR_ENDPOINT, headers=headers, json=body
        ) as resp:
            data = await resp.json()
            # Azure returns list of translated objects
            translated = data[0]["translations"][0]["text"]
            return translated


async def live_caption_translate(audio_iterator) -> None:
    """Consume an async iterator yielding normalized caption dicts and print translations."""
    client = get_speech_client(PROVIDER)
    async for caption in audio_iterator:
        # Assume caption is already normalized by speech_models.normalize_response
        translated = await translate_text(caption["transcript"])
        print(f"[TRANSLATED] {PROVIDER} => {TARGET_LANG}: {translated}")


# Example usage with stream_microphone (uncomment to test)
# async def main():
#     async for cap in stream_microphone():
#         print(cap)
#         await live_caption_translate([cap])  # treat each as a caption chunk
# asyncio.run(main())
