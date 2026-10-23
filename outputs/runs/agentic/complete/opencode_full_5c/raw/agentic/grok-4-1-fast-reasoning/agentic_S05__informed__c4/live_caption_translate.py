import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
import deepl


async def live_caption_translate(
    caption_stream: AsyncIterable[str], target_lang: str = "ES", source_lang: str = "EN"
) -> AsyncGenerator[str, None]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY must be set")
    translator = deepl.Translator(auth_key)
    async for caption in caption_stream:
        if caption.strip():
            result = translator.translate_text(
                caption, target_lang=target_lang, source_lang=source_lang
            )
            yield result.text
        else:
            yield caption
