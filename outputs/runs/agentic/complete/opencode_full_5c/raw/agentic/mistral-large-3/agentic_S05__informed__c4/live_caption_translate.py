import os
from typing import AsyncGenerator

from google.cloud import translate_v2 as translate


class LiveCaptionTranslator:
    """Translate live captions into another language using Google Cloud Translation."""

    def __init__(self, target_language: str = "es"):
        self.client = translate.Client()
        self.target_language = target_language

    async def translate_captions(
        self, captions: AsyncGenerator[str, None]
    ) -> AsyncGenerator[str, None]:
        """Translate live captions into the target language."""
        async for caption in captions:
            result = self.client.translate(
                caption, target_language=self.target_language
            )
            yield result["translatedText"]
