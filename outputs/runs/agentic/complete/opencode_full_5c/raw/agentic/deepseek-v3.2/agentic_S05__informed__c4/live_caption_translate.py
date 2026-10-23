import os
from typing import List, Dict, Any
import google.cloud.translate_v2 as translate


class LiveCaptionTranslator:
    def __init__(self, target_language: str = "es"):
        self.client = translate.Client()
        self.target_language = target_language

    def translate_caption(
        self, caption_text: str, source_language: str = "en"
    ) -> Dict[str, Any]:
        """Translate a single caption."""
        try:
            result = self.client.translate(
                caption_text,
                target_language=self.target_language,
                source_language=source_language,
                format_="text",
            )

            return {
                "original": caption_text,
                "translated": result["translatedText"],
                "source_language": source_language,
                "target_language": self.target_language,
                "detected_source_language": result.get(
                    "detectedSourceLanguage", source_language
                ),
            }
        except Exception as e:
            print(f"Translation error: {e}")
            return {
                "original": caption_text,
                "translated": caption_text,  # Fallback to original
                "source_language": source_language,
                "target_language": self.target_language,
                "error": str(e),
            }

    def translate_captions_batch(
        self, captions: List[str], source_language: str = "en"
    ) -> List[Dict[str, Any]]:
        """Translate multiple captions in batch."""
        if not captions:
            return []

        try:
            results = self.client.translate(
                captions,
                target_language=self.target_language,
                source_language=source_language,
                format_="text",
            )

            translated = []
            for i, result in enumerate(results):
                translated.append(
                    {
                        "original": captions[i],
                        "translated": result["translatedText"],
                        "source_language": source_language,
                        "target_language": self.target_language,
                        "detected_source_language": result.get(
                            "detectedSourceLanguage", source_language
                        ),
                    }
                )

            return translated
        except Exception as e:
            print(f"Batch translation error: {e}")
            return [
                self.translate_caption(caption, source_language) for caption in captions
            ]

    def detect_language(self, text: str) -> str:
        """Detect the language of text."""
        try:
            result = self.client.detect_language(text)
            return result["language"]
        except Exception as e:
            print(f"Language detection error: {e}")
            return "en"

    def translate_with_detection(self, caption_text: str) -> Dict[str, Any]:
        """Translate caption with automatic language detection."""
        detected_lang = self.detect_language(caption_text)
        return self.translate_caption(caption_text, detected_lang)


async def process_live_caption_stream(
    caption_stream, translator: LiveCaptionTranslator
):
    """Process a stream of live captions and translate them."""
    async for caption in caption_stream:
        if caption.get("is_final", False):
            caption_text = caption.get("text", "")

            if caption_text.strip():
                translation = translator.translate_caption(
                    caption_text, source_language=caption.get("language_code", "en")
                )

                yield {"original_caption": caption, "translation": translation}


class MultiLanguageTranslator:
    def __init__(self):
        self.client = translate.Client()
        self.supported_languages = self._get_supported_languages()

    def _get_supported_languages(self) -> List[Dict[str, str]]:
        """Get list of supported languages."""
        try:
            languages = self.client.get_languages()
            return languages
        except Exception as e:
            print(f"Error getting supported languages: {e}")
            return []

    def translate_to_multiple(
        self, text: str, source_lang: str, target_langs: List[str]
    ) -> Dict[str, Any]:
        """Translate text to multiple target languages."""
        results = {}

        for target_lang in target_langs:
            try:
                result = self.client.translate(
                    text, target_language=target_lang, source_language=source_lang
                )
                results[target_lang] = result["translatedText"]
            except Exception as e:
                print(f"Error translating to {target_lang}: {e}")
                results[target_lang] = text  # Fallback

        return {
            "original": text,
            "source_language": source_lang,
            "translations": results,
        }


if __name__ == "__main__":
    translator = LiveCaptionTranslator(target_language="es")

    test_captions = [
        "Hello, welcome to the meeting.",
        "Let's discuss the quarterly results.",
        "The project deadline is next Friday.",
    ]

    for caption in test_captions:
        result = translator.translate_caption(caption)
        print(f"Original: {result['original']}")
        print(f"Translated: {result['translated']}")
        print(f"Detected: {result['detected_source_language']}")
        print()
