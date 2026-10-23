import asyncio
import os
import deepl
from typing import AsyncGenerator, AsyncIterable

async def live_caption_translate(captions: AsyncIterable[str], target_lang: str = "ES") -> AsyncGenerator[str, None]:
    auth_key = os.getenv('DEEPL_AUTH_KEY')
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not set")
    translator = deepl.Translator(auth_key)

    async for caption in captions:
        if caption.strip():
            result = translator.translate_text(caption.strip(), target_lang=deepl.TargetLanguage(target_lang))
            yield result.text
        else:
            yield caption