import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
from deepl import Translator


async def translate_live_captions(
    caption_iter: AsyncIterable[str], target_lang: str = "ES"
) -> AsyncGenerator[str, None]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")
    translator = Translator(auth_key)
    async for caption in caption_iter:
        result = await asyncio.to_thread(
            translator.translate_text, caption, target_lang=target_lang
        )
        yield result.text
