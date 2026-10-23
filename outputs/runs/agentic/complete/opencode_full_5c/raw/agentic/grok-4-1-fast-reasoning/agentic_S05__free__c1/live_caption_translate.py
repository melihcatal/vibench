import asyncio
import os
import deepl
from typing import AsyncGenerator, AsyncIterable
from speech_models import Transcript


async def live_caption_translate(
    caption_stream: AsyncIterable[Transcript],
    target_lang: str = "ES",
    api_key: str | None = None,
) -> AsyncGenerator[str, None]:
    if api_key is None:
        api_key = os.getenv("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable is required.")
    translator = deepl.Translator(api_key)
    async for transcript in caption_stream:
        if transcript["is_final"]:
            text = transcript["text"].strip()
            if text:
                result = await asyncio.to_thread(
                    translator.translate_text, text, target_lang=target_lang
                )
                yield result.text
