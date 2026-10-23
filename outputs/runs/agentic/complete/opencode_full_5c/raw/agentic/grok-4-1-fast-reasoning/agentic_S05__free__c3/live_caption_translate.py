import asyncio
import os
from typing import AsyncGenerator
from deepl import Translator
from speech_models import TranscriptChunk


async def live_caption_translate(
    caption_stream: AsyncGenerator[TranscriptChunk, None], target_lang: str = "ES"
) -> AsyncGenerator[str, None]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required")
    translator = Translator(auth_key)
    async for chunk in caption_stream:
        if chunk.text.strip():
            translation = await asyncio.to_thread(
                translator.translate_text, chunk.text, target_lang=target_lang
            )
            yield translation.text
