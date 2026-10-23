from google.cloud import translate_v2 as translate
from typing import Generator, Tuple, Optional
import asyncio


class LiveCaptionTranslator:
    def __init__(
        self, target_language: str = "es", credentials_path: Optional[str] = None
    ):
        self.target_language = target_language
        self.client = (
            translate.Client.from_service_account_json(credentials_path)
            if credentials_path
            else translate.Client()
        )
        self.translation_cache = {}

    def translate_caption(
        self, caption_text: str, source_language: Optional[str] = None
    ) -> str:
        if not caption_text.strip():
            return caption_text

        cache_key = f"{source_language or 'auto'}:{self.target_language}:{caption_text}"
        if cache_key in self.translation_cache:
            return self.translation_cache[cache_key]

        try:
            if source_language:
                result = self.client.translate(
                    caption_text,
                    target_language=self.target_language,
                    source_language=source_language,
                )
            else:
                result = self.client.translate(
                    caption_text, target_language=self.target_language
                )

            translated_text = result["translatedText"]
            self.translation_cache[cache_key] = translated_text
            return translated_text

        except Exception as e:
            print(f"Translation error: {e}")
            return caption_text

    def stream_translate_captions(
        self,
        caption_stream: Generator[Tuple[str, bool], None, None],
        source_language: Optional[str] = None,
    ) -> Generator[Tuple[str, str, bool], None, None]:

        for caption, is_final in caption_stream:
            if not caption.strip():
                continue

            translated = self.translate_caption(caption, source_language)
            yield caption, translated, is_final

    async def async_translate_caption(
        self, caption_text: str, source_language: Optional[str] = None
    ) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, lambda: self.translate_caption(caption_text, source_language)
        )

    async def async_stream_translate(
        self, caption_stream, source_language: Optional[str] = None
    ):
        async for caption, is_final in caption_stream:
            if not caption.strip():
                continue

            translated = await self.async_translate_caption(caption, source_language)
            yield caption, translated, is_final


class MultiLanguageTranslator:
    def __init__(self, credentials_path: Optional[str] = None):
        self.client = (
            translate.Client.from_service_account_json(credentials_path)
            if credentials_path
            else translate.Client()
        )

    def translate_to_multiple(
        self, text: str, target_languages: list, source_language: Optional[str] = None
    ) -> dict:
        translations = {}

        for lang in target_languages:
            try:
                if source_language:
                    result = self.client.translate(
                        text, target_language=lang, source_language=source_language
                    )
                else:
                    result = self.client.translate(text, target_language=lang)

                translations[lang] = result["translatedText"]
            except Exception as e:
                print(f"Translation to {lang} failed: {e}")
                translations[lang] = text

        return translations

    def detect_language(self, text: str) -> dict:
        try:
            result = self.client.detect_language(text)
            return {
                "language": result["language"],
                "confidence": result.get("confidence", 0.0),
            }
        except Exception as e:
            print(f"Language detection failed: {e}")
            return {"language": "en", "confidence": 0.0}


def create_live_translation_pipeline(
    caption_stream: Generator[Tuple[str, bool], None, None],
    target_language: str = "es",
    credentials_path: Optional[str] = None,
) -> Generator[Tuple[str, str, bool], None, None]:

    translator = LiveCaptionTranslator(target_language, credentials_path)

    for original, translated, is_final in translator.stream_translate_captions(
        caption_stream
    ):
        yield original, translated, is_final


def translate_final_captions_only(
    caption_stream: Generator[Tuple[str, bool], None, None],
    target_language: str = "es",
    credentials_path: Optional[str] = None,
) -> Generator[Tuple[str, str], None, None]:

    translator = LiveCaptionTranslator(target_language, credentials_path)

    for caption, is_final in caption_stream:
        if is_final and caption.strip():
            translated = translator.translate_caption(caption)
            yield caption, translated
