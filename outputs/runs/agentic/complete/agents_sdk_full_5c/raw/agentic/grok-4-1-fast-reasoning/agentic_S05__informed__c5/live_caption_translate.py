import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
from deepl import Translator

_translator = None

def get_translator() -> Translator:
    global _translator
    if _translator is None:
        auth_key = os.getenv('DEEPL_AUTH_KEY')
        if not auth_key:
            raise ValueError('DEEPL_AUTH_KEY environment variable is required.')
        _translator = Translator(auth_key)
    return _translator

async def translate_live_captions(
    captions: AsyncIterable[str],
    target_language: str = 'ES'
) -> AsyncGenerator[str, None]:
    translator = get_translator()
    async for caption in captions:
        result = await asyncio.to_thread(
            translator.translate_text,
            caption,
            target_lang=target_language
        )
        yield result.text
