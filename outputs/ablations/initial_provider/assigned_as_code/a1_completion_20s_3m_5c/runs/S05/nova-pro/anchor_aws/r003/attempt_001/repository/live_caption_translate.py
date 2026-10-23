import asyncio
import aiohttp

from google.cloud import translate_v2 as translate

async def translate_captions(captions, target_language):
    client = translate.Client()
    translated_captions = []
    async with aiohttp.ClientSession() as session:
        for caption in captions:
            translation = await client.translate(caption['text'], target_language=target_language)
            translated_captions.append({'text': translation['translatedText'], 'is_final': caption['is_final']})
    return translated_captions