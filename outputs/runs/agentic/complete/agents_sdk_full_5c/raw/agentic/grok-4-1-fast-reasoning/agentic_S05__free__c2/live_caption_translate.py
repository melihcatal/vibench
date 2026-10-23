import asyncio
import os
import deepl
from typing import AsyncGenerator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")
if not DEEPL_AUTH_KEY:
    raise ValueError("DEEPL_AUTH_KEY environment variable is required.")

translator = deepl.Translator(DEEPL_AUTH_KEY)

async def live_caption_translate(caption_generator, target_language="ES") -> AsyncGenerator[str, None]:
    async for caption in caption_generator:
        result = translator.translate_text(caption, target_lang=target_language)
        yield result.text