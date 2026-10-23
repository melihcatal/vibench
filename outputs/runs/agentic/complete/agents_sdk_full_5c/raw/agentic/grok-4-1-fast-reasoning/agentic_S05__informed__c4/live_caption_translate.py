import os
import asyncio
import deepl
from typing import AsyncGenerator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPGRAM_API_KEY:
    raise ValueError("DEEPL_AUTH_KEY environment variable is required.")

translator = deepl.Translator(DEEPL_AUTH_KEY)

async def translate_live_captions(text_generator: AsyncGenerator[str, None], target_lang: str = "es") -> AsyncGenerator[str, None]:
    async for text in text_generator:
        result = await asyncio.to_thread(
            translator.translate_text, text, target_lang=target_lang
        )
        yield result.text
