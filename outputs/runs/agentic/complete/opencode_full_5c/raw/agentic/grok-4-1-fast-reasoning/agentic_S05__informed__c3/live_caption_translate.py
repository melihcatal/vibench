import asyncio
import os
from typing import AsyncGenerator, AsyncIterator
from deepl import Translator


async def translate_live_captions(
    captions: AsyncIterator[str], target_lang: str = "ES"
) -> AsyncGenerator[str, None]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY required")
    translator = Translator(auth_key)
    loop = asyncio.get_event_loop()
    async for caption in captions:
        result = await loop.run_in_executor(
            None, translator.translate_text, caption, target_lang=target_lang
        )
        yield result.text
