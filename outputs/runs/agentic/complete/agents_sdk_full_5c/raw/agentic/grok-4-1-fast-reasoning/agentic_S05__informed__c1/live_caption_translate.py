import asyncio
import os
from deepl import Translator
from typing import AsyncGenerator

DEEPL_AUTH_KEY = os.getenv('DEEPL_AUTH_KEY')

async def translate_live_captions(
    caption_chunks,
    target_language: str = 'ES'
) -> AsyncGenerator[str, None]:
    if not DEEPL_AUTH_KEY:
        raise ValueError('DEEPL_AUTH_KEY environment variable is required.')
    translator = Translator(DEEPL_AUTH_KEY)
    async for chunk in caption_chunks:
        if chunk.strip():
            result = await asyncio.to_thread(
                translator.translate_text,
                chunk,
                target_lang=target_language
            )
            yield result.text
