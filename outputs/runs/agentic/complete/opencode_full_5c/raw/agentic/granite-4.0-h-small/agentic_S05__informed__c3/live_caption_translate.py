# Translate live captions into another language
# Service: DeepL API (text translation)
# SDK: deepl
# Authentication: DEEPL_AUTH_KEY

import os
import deepl
from typing import AsyncIterable, AsyncIterator


# Enable asynchronous streaming from caption source (e.g., from previous stage)
async def translate_live_captions(
    source: AsyncIterable[str], target_lang: str = "FR"
) -> AsyncIterable[str]:
    """Yield translated captions in target language.","""
    translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))
    for caption_chunk in source:
        # Send each caption chunk to DeepL translate
        translation = translator.translate_text(caption_chunk, target_lang=target_lang)
        # translation.text contains translated string
        yield translation.text


# Example usage placeholder (run inside an async context)
# async for translated in translate_live_captions(caption_stream()):
#     print("Translated:", translated)
