from google.cloud import translate_v2 as translate
from typing import Generator, Dict, Any, Optional
import asyncio
import aiohttp


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es", source_language: str = "en"):
        self.client = translate.Client()
        self.target_language = target_language
        self.source_language = source_language

    def translate_text(self, text: str) -> str:
        if not text.strip():
            return ""

        try:
            result = self.client.translate(
                text,
                target_language=self.target_language,
                source_language=self.source_language,
            )
            return result["translatedText"]
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    async def translate_text_async(self, text: str) -> str:
        if not text.strip():
            return ""

        try:
            result = await asyncio.to_thread(
                self.client.translate,
                text,
                target_language=self.target_language,
                source_language=self.source_language,
            )
            return result["translatedText"]
        except Exception as e:
            print(f"Async translation error: {e}")
            return text

    def translate_caption_stream(
        self, caption_stream: Generator[Dict[str, Any], None, None]
    ) -> Generator[Dict[str, Any], None, None]:
        for caption in caption_stream:
            transcript = caption.get("transcript", "")
            is_final = caption.get("is_final", False)

            translated_text = self.translate_text(transcript)

            translated_caption = caption.copy()
            translated_caption["transcript"] = translated_text
            translated_caption["original_transcript"] = transcript
            translated_caption["target_language"] = self.target_language
            translated_caption["source_language"] = self.source_language
            translated_caption["is_translated"] = True

            yield translated_caption

    async def translate_caption_stream_async(
        self, caption_stream
    ) -> Generator[Dict[str, Any], None, None]:
        async for caption in caption_stream:
            transcript = caption.get("transcript", "")
            is_final = caption.get("is_final", False)

            translated_text = await self.translate_text_async(transcript)

            translated_caption = caption.copy()
            translated_caption["transcript"] = translated_text
            translated_caption["original_transcript"] = transcript
            translated_caption["target_language"] = self.target_language
            translated_caption["source_language"] = self.source_language
            translated_caption["is_translated"] = True

            yield translated_caption


def create_live_translation_pipeline(
    caption_stream: Generator[Dict[str, Any], None, None],
    target_language: str = "es",
    source_language: str = "en",
) -> Generator[Dict[str, Any], None, None]:

    translator = LiveCaptionTranslator(
        target_language=target_language, source_language=source_language
    )

    return translator.translate_caption_stream(caption_stream)


async def create_async_live_translation_pipeline(
    caption_stream, target_language: str = "es", source_language: str = "en"
):

    translator = LiveCaptionTranslator(
        target_language=target_language, source_language=source_language
    )

    async for translated in translator.translate_caption_stream_async(caption_stream):
        yield translated


SUPPORTED_TRANSLATION_LANGUAGES = {
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "ja": "Japanese",
    "ko": "Korean",
    "zh": "Chinese",
    "pt": "Portuguese",
    "ru": "Russian",
    "ar": "Arabic",
    "hi": "Hindi",
}


def get_supported_target_languages():
    return list(SUPPORTED_TRANSLATION_LANGUAGES.keys())


def translate_live_captions(
    caption_stream: Generator[Dict[str, Any], None, None], target_language: str = "es"
) -> Generator[Dict[str, Any], None, None]:

    if target_language not in SUPPORTED_TRANSLATION_LANGUAGES:
        raise ValueError(f"Unsupported target language: {target_language}")

    return create_live_translation_pipeline(
        caption_stream, target_language=target_language, source_language="en"
    )
