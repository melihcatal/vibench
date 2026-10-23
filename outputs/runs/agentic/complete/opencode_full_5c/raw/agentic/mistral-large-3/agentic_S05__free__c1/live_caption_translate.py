from google.cloud import translate_v2 as translate
from typing import AsyncIterator


class LiveCaptionTranslator:
    """Translates live captions into another language using Google Cloud Translation."""

    def __init__(self, target_language: str = "es"):
        self.client = translate.Client()
        self.target_language = target_language

    async def translate_captions(
        self, caption_stream: AsyncIterator[str]
    ) -> AsyncIterator[str]:
        """Translates a stream of captions into the target language."""
        async for caption in caption_stream:
            result = self.client.translate(
                caption, target_language=self.target_language
            )
            yield result["translatedText"]
