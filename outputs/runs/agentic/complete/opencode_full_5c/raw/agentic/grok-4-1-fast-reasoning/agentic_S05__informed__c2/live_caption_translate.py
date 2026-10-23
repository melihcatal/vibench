import asyncio
import os
from typing import AsyncGenerator
from deepl import Translator

DEEPL_AUTH_KEY = os.getenv("DEEPL_AUTH_KEY")


async def translate_live_captions(
    caption_stream: AsyncGenerator[str, None], target_lang: str = "ES"
) -> AsyncGenerator[str, None]:
    translator = Translator(DEEPL_AUTH_KEY)
    async for caption in caption_stream:
        translated = await asyncio.to_thread(
            translator.translate_text, caption, target_lang=target_lang
        )
        yield translated.text
