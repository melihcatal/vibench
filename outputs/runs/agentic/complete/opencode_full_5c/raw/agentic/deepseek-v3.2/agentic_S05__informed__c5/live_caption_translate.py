import os
import asyncio
from typing import List, Optional
import deepl


class LiveCaptionTranslator:
    """Translate live captions into another language using DeepL."""

    def __init__(self, target_language: str = "DE"):
        self.auth_key = os.getenv("DEEPL_AUTH_KEY")
        if not self.auth_key:
            raise ValueError("DEEPL_AUTH_KEY environment variable is required")

        self.translator = deepl.Translator(self.auth_key)
        self.target_language = target_language

        # Validate target language
        self._validate_language(target_language)

    def _validate_language(self, language: str):
        """Validate that the target language is supported by DeepL."""
        try:
            usage = self.translator.get_usage()
            # DeepL supports many languages, we'll check against common ones
            supported_languages = [
                "BG",
                "CS",
                "DA",
                "DE",
                "EL",
                "EN",
                "ES",
                "ET",
                "FI",
                "FR",
                "HU",
                "ID",
                "IT",
                "JA",
                "KO",
                "LT",
                "LV",
                "NB",
                "NL",
                "PL",
                "PT",
                "RO",
                "RU",
                "SK",
                "SL",
                "SV",
                "TR",
                "UK",
                "ZH",
            ]

            if language.upper() not in supported_languages:
                print(
                    f"Warning: Language {language} may not be fully supported by DeepL"
                )
        except Exception as e:
            print(f"Warning: Could not validate language {language}: {e}")

    async def translate_caption(
        self, caption_text: str, source_language: Optional[str] = None
    ) -> str:
        """Translate a single caption text."""
        try:
            if source_language:
                result = self.translator.translate_text(
                    caption_text,
                    source_lang=source_language,
                    target_lang=self.target_language,
                )
            else:
                result = self.translator.translate_text(
                    caption_text, target_lang=self.target_language
                )

            return result.text
        except Exception as e:
            print(f"Translation error: {e}")
            return caption_text  # Return original on error

    async def translate_captions_stream(
        self, caption_stream, source_language: Optional[str] = None
    ):
        """Translate a stream of captions."""
        async for caption in caption_stream:
            if caption and caption.strip():
                translated = await self.translate_caption(caption, source_language)
                yield translated
            else:
                yield caption

    def get_supported_languages(self) -> List[str]:
        """Get list of languages supported by DeepL."""
        return [
            "BG",
            "CS",
            "DA",
            "DE",
            "EL",
            "EN",
            "ES",
            "ET",
            "FI",
            "FR",
            "HU",
            "ID",
            "IT",
            "JA",
            "KO",
            "LT",
            "LV",
            "NB",
            "NL",
            "PL",
            "PT",
            "RO",
            "RU",
            "SK",
            "SL",
            "SV",
            "TR",
            "UK",
            "ZH",
        ]

    def get_language_name(self, language_code: str) -> str:
        """Get human-readable language name from code."""
        language_names = {
            "BG": "Bulgarian",
            "CS": "Czech",
            "DA": "Danish",
            "DE": "German",
            "EL": "Greek",
            "EN": "English",
            "ES": "Spanish",
            "ET": "Estonian",
            "FI": "Finnish",
            "FR": "French",
            "HU": "Hungarian",
            "ID": "Indonesian",
            "IT": "Italian",
            "JA": "Japanese",
            "KO": "Korean",
            "LT": "Lithuanian",
            "LV": "Latvian",
            "NB": "Norwegian",
            "NL": "Dutch",
            "PL": "Polish",
            "PT": "Portuguese",
            "RO": "Romanian",
            "RU": "Russian",
            "SK": "Slovak",
            "SL": "Slovenian",
            "SV": "Swedish",
            "TR": "Turkish",
            "UK": "Ukrainian",
            "ZH": "Chinese",
        }
        return language_names.get(language_code.upper(), language_code)


async def mock_caption_stream():
    """Mock caption stream for testing."""
    captions = [
        "Hello everyone, welcome to the meeting.",
        "Today we will discuss the quarterly results.",
        "The sales numbers have exceeded expectations.",
        "We need to focus on customer satisfaction.",
        "Thank you for your attention.",
    ]

    for caption in captions:
        yield caption
        await asyncio.sleep(0.5)


async def test_live_translation():
    """Test live caption translation."""
    print("Testing live caption translation with DeepL...")

    # Create translator for German
    translator = LiveCaptionTranslator(target_language="DE")

    print(f"Target language: {translator.get_language_name('DE')}")
    print(f"Supported languages: {translator.get_supported_languages()}")

    # Translate individual captions
    test_captions = [
        "Good morning, how are you?",
        "The project deadline is next Friday.",
        "We need to improve our communication.",
    ]

    print("\nTranslating individual captions:")
    for caption in test_captions:
        translated = await translator.translate_caption(caption)
        print(f"Original: {caption}")
        print(f"Translated: {translated}")
        print()

    # Test streaming translation
    print("Testing streaming translation:")
    async for translated in translator.translate_captions_stream(mock_caption_stream()):
        print(f"Translated caption: {translated}")


if __name__ == "__main__":
    asyncio.run(test_live_translation())
