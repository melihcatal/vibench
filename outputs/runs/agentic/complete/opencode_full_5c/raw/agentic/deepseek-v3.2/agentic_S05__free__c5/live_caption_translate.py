from typing import Optional, Dict, Any, Generator
import asyncio
from google.cloud import translate_v2 as translate


class LiveCaptionTranslator:
    def __init__(
        self,
        source_language: str = "en",
        target_language: str = "es",
        credentials_path: Optional[str] = None,
    ):

        self.source_language = source_language
        self.target_language = target_language

        if credentials_path:
            self.translate_client = translate.Client.from_service_account_json(
                credentials_path
            )
        else:
            self.translate_client = translate.Client()

        self.supported_languages = self._get_supported_languages()

    def _get_supported_languages(self) -> Dict[str, str]:
        try:
            languages = self.translate_client.get_languages()
            return {lang["language"]: lang["name"] for lang in languages}
        except Exception as e:
            print(f"Failed to fetch supported languages: {e}")
            return {
                "en": "English",
                "es": "Spanish",
                "fr": "French",
                "de": "German",
                "ja": "Japanese",
                "ko": "Korean",
                "zh": "Chinese",
                "pt": "Portuguese",
                "ru": "Russian",
                "it": "Italian",
            }

    def translate_text(
        self,
        text: str,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
    ) -> Dict[str, Any]:

        source = source_language or self.source_language
        target = target_language or self.target_language

        if source not in self.supported_languages:
            raise ValueError(f"Unsupported source language: {source}")
        if target not in self.supported_languages:
            raise ValueError(f"Unsupported target language: {target}")

        try:
            result = self.translate_client.translate(
                text, source_language=source, target_language=target, format_="text"
            )

            return {
                "original_text": text,
                "translated_text": result["translatedText"],
                "source_language": source,
                "target_language": target,
                "detected_language": result.get("detectedSourceLanguage", source),
                "model": "nmt",  # Google's Neural Machine Translation
            }
        except Exception as e:
            print(f"Translation failed: {e}")
            return {
                "original_text": text,
                "translated_text": text,
                "source_language": source,
                "target_language": target,
                "error": str(e),
            }

    def translate_caption_stream(
        self,
        caption_stream: Generator[Dict[str, Any], None, None],
        translate_final_only: bool = True,
    ) -> Generator[Dict[str, Any], None, None]:

        for caption in caption_stream:
            if translate_final_only and not caption.get("is_final", False):
                yield {**caption, "translated": False, "translated_text": None}
                continue

            transcript = caption.get("transcript", "")
            if not transcript.strip():
                yield {**caption, "translated": False, "translated_text": None}
                continue

            translation = self.translate_text(
                transcript,
                source_language=caption.get("language_code", self.source_language),
                target_language=self.target_language,
            )

            yield {
                **caption,
                "translated": True,
                "translated_text": translation["translated_text"],
                "translation_source_lang": translation["source_language"],
                "translation_target_lang": translation["target_language"],
                "detected_language": translation.get("detected_language"),
                "translation_model": translation.get("model"),
            }

    async def translate_caption_stream_async(
        self, caption_stream, translate_final_only: bool = True
    ):

        async for caption in caption_stream:
            if translate_final_only and not caption.get("is_final", False):
                yield {**caption, "translated": False, "translated_text": None}
                continue

            transcript = caption.get("transcript", "")
            if not transcript.strip():
                yield {**caption, "translated": False, "translated_text": None}
                continue

            loop = asyncio.get_event_loop()
            translation = await loop.run_in_executor(
                None,
                self.translate_text,
                transcript,
                caption.get("language_code", self.source_language),
                self.target_language,
            )

            yield {
                **caption,
                "translated": True,
                "translated_text": translation["translated_text"],
                "translation_source_lang": translation["source_language"],
                "translation_target_lang": translation["target_language"],
                "detected_language": translation.get("detected_language"),
                "translation_model": translation.get("model"),
            }

    def batch_translate(
        self,
        texts: list,
        source_language: Optional[str] = None,
        target_language: Optional[str] = None,
    ) -> list:

        source = source_language or self.source_language
        target = target_language or self.target_language

        results = []
        for text in texts:
            result = self.translate_text(text, source, target)
            results.append(result)

        return results

    def get_language_name(self, language_code: str) -> str:
        return self.supported_languages.get(language_code, language_code)

    def switch_target_language(self, new_target_language: str):
        if new_target_language not in self.supported_languages:
            raise ValueError(f"Unsupported target language: {new_target_language}")
        self.target_language = new_target_language


class BilingualCaptionDisplay:
    def __init__(self, translator: LiveCaptionTranslator):
        self.translator = translator

    def format_bilingual_caption(
        self, original_caption: Dict[str, Any], translated_caption: Dict[str, Any]
    ) -> str:

        original_text = original_caption.get("transcript", "")
        translated_text = translated_caption.get("translated_text", "")

        if not translated_text:
            return original_text

        source_lang = self.translator.get_language_name(
            original_caption.get("language_code", "en")
        )
        target_lang = self.translator.get_language_name(self.translator.target_language)

        prefix = "[FINAL]" if original_caption.get("is_final", False) else "[INTERIM]"

        return f"{prefix}\n{source_lang}: {original_text}\n{target_lang}: {translated_text}"

    def display_stream(self, caption_stream):
        for caption in self.translator.translate_caption_stream(caption_stream):
            if caption.get("translated", False):
                formatted = self.format_bilingual_caption(caption, caption)
                print(formatted)
                print("-" * 50)
            else:
                prefix = "[FINAL]" if caption.get("is_final", False) else "[INTERIM]"
                print(f"{prefix} {caption.get('transcript', '')}")


def example_caption_generator():
    captions = [
        {
            "transcript": "Hello everyone, welcome to the meeting.",
            "is_final": True,
            "language_code": "en",
        },
        {
            "transcript": "Today we will discuss the quarterly results.",
            "is_final": True,
            "language_code": "en",
        },
        {
            "transcript": "The revenue has increased by",
            "is_final": False,
            "language_code": "en",
        },
        {
            "transcript": "The revenue has increased by 15% this quarter.",
            "is_final": True,
            "language_code": "en",
        },
    ]

    for caption in captions:
        yield caption


if __name__ == "__main__":
    translator = LiveCaptionTranslator(source_language="en", target_language="es")

    caption_gen = example_caption_generator()

    print("Starting live caption translation (English → Spanish):")
    print("=" * 60)

    for translated_caption in translator.translate_caption_stream(caption_gen):
        if translated_caption["translated"]:
            print(f"Original: {translated_caption['transcript']}")
            print(f"Translated: {translated_caption['translated_text']}")
            print(f"Language: {translated_caption['detected_language']}")
            print("-" * 40)
