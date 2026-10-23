import asyncio
import os
from typing import AsyncGenerator, AsyncIterable
from deepl import Translator
from speech_models import TranscriptChunk


async def translate_live_captions(
    transcripts: AsyncIterable[TranscriptChunk], target_language: str = "ES"
) -> AsyncGenerator[str, None]:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is required.")

    translator = Translator(auth_key)

    async for chunk in transcripts:
        if chunk.is_final and chunk.text.strip():
            result = translator.translate_text(chunk.text, target_lang=target_language)
            yield result.text
