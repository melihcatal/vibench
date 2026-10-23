import os
import deepl
from typing import AsyncIterator
from speech_models import TranscriptChunk, TranscriptStream

translator = deepl.Translator(os.getenv("DEEPL_AUTH_KEY"))


async def translate_live_captions(
    stream: TranscriptStream, target_lang: str = "FR"
) -> AsyncIterator[str]:
    async for chunk in stream:
        result = translator.translate_text(
            chunk["transcript"], target_lang=deepl.TargetLanguage(target_lang)
        )
        yield result.text
