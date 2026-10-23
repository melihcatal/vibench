from typing import Optional

from google.cloud.translate_v2 import Client as TranslateClient
from google.cloud.speech_v2.types import cloud_speech

from speech_models import RecognitionResult


GOOGLE_TRANSLATE_API_ENDPOINT = "translation.googleapis.com"


def create_translate_client() -> TranslateClient:
    return TranslateClient()


def translate_text(
    text: str,
    target_language: str,
    source_language: Optional[str] = None,
    format_type: str = "text",
) -> str:
    client = create_translate_client()
    result = client.translate(
        text,
        target_language=target_language,
        source_language=source_language,
        format_=format_type,
    )
    return result.get("translatedText", text)


async def translate_live_caption(
    result: RecognitionResult,
    target_language: str,
    source_language: Optional[str] = None,
) -> str:
    transcript = result.best_transcript
    if not transcript:
        return ""

    translated = translate_text(
        text=transcript,
        target_language=target_language,
        source_language=source_language or result.language_code,
    )
    return translated


async def translate_live_captions_stream(
    results,
    target_language: str,
    source_language: Optional[str] = None,
    on_translated=None,
):
    async for result in results:
        translated = await translate_live_caption(
            result=result,
            target_language=target_language,
            source_language=source_language,
        )
        if on_translated and translated:
            on_translated(result, translated)
        yield translated


class LiveCaptionTranslator:
    def __init__(
        self,
        target_language: str,
        source_language: Optional[str] = None,
    ):
        self.target_language = target_language
        self.source_language = source_language
        self._client = create_translate_client()
        self._translation_cache = {}

    def translate(self, text: str) -> str:
        if text in self._translation_cache:
            return self._translation_cache[text]

        translated = translate_text(
            text=text,
            target_language=self.target_language,
            source_language=self.source_language,
        )
        self._translation_cache[text] = translated
        return translated

    def translate_result(self, result: RecognitionResult) -> str:
        return self.translate(result.best_transcript)

    def clear_cache(self):
        self._translation_cache.clear()
