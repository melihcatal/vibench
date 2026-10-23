import asyncio
from typing import AsyncGenerator
import deepl
import os

async def translate_live_captions(captions: AsyncGenerator[str, None], target_lang: str = &quot;ES&quot;) -> AsyncGenerator[str, None]:
    auth_key = os.getenv(&quot;DEEPL_AUTH_KEY&quot;)
    if not auth_key:
        raise ValueError(&quot;DEEPL_AUTH_KEY environment variable is required&quot;)
    translator = deepl.Translator(auth_key)
    async for caption in captions:
        if caption.strip():
            result = translator.translate_text(caption, target_lang=deepl.TargetLanguage(target_lang))
            yield result.text
