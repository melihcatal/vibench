import os
import httpx
from typing import AsyncGenerator

from speech_models import TranscriptResult


async def translate_caption_chunk(text: str, target_language: str = "es") -> str:
    translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    translator_region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not translator_key or not translator_region:
        raise ValueError(
            "AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables must be set"
        )

    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = "/translate"
    params = {"api-version": "3.0", "to": target_language}
    headers = {
        "Ocp-Apim-Subscription-Key": translator_key,
        "Ocp-Apim-Subscription-Region": translator_region,
        "Content-type": "application/json",
    }
    body = [{"text": text}]

    async with httpx.AsyncClient() as client:
        response = await client.post(
            endpoint + path, params=params, headers=headers, json=body
        )
        response.raise_for_status()
        translation_result = response.json()
        if (
            translation_result
            and len(translation_result) > 0
            and "translations" in translation_result[0]
        ):
            return translation_result[0]["translations"][0]["text"]
        return text


async def live_caption_translate(
    caption_stream: AsyncGenerator[TranscriptResult, None], target_language: str = "es"
):
    print(f"Translating live captions to {target_language}...")
    async for caption_result in caption_stream:
        if caption_result.is_final and caption_result.text.strip():
            translated_text = await translate_caption_chunk(
                caption_result.text, target_language
            )
            yield TranscriptResult(
                text=translated_text,
                is_final=True,
                confidence=caption_result.confidence,
            )
        else:
            yield caption_result
