"""
alt_text_translate.py - Translate generated image descriptions.

Provider: DeepL API (api.deepl.com)
Provider SDK: deepl
Provider Identifying Signals: deepl import, DEEPL_ env vars,
                              api.deepl.com hostname, DeepL client
"""

import os
import json
from typing import Optional, List, Dict

import deepl


# DeepL supported language codes
SUPPORTED_LANGUAGES = {
    "en": "English",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "it": "Italian",
    "nl": "Dutch",
    "pl": "Polish",
    "pt": "Portuguese",
    "ru": "Russian",
    "ja": "Japanese",
    "zh": "Chinese",
    "ko": "Korean",
    "ar": "Arabic",
    "bg": "Bulgarian",
    "cs": "Czech",
    "da": "Danish",
    "el": "Greek",
    "fi": "Finnish",
    "hu": "Hungarian",
    "id": "Indonesian",
    "lt": "Lithuanian",
    "lv": "Latvian",
    "no": "Norwegian",
    "ro": "Romanian",
    "sk": "Slovak",
    "sl": "Slovenian",
    "sv": "Swedish",
    "tr": "Turkish",
    "uk": "Ukrainian",
}


class DeepLTranslator:
    """
    Translate image descriptions using DeepL Translation API.
    
    Provider: DeepL API
    Endpoint: api.deepl.com
    SDK: deepl (official DeepL Python library)
    """

    FREE_API_URL = "https://api-free.deepl.com"
    PRO_API_URL = "https://api.deepl.com"

    def __init__(
        self,
        api_key: Optional[str] = None,
        server_url: Optional[str] = None,
    ):
        self.api_key = api_key or os.environ.get("DEEPL_AUTH_KEY", "")
        
        if server_url:
            self.server_url = server_url
        elif self.api_key.endswith(":fx"):
            self.server_url = self.FREE_API_URL
        else:
            self.server_url = os.environ.get(
                "DEEPL_SERVER_URL", self.PRO_API_URL
            )

        self.client = deepl.Translator(
            self.api_key,
            server_url=self.server_url,
        )

    def translate_description(
        self,
        text: str,
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: str = "default",
    ) -> Dict[str, str]:
        """
        Translate a single image description to the target language.

        Args:
            text: The image description/alt-text to translate.
            target_lang: Target language code (e.g., 'de', 'fr', 'ja').
            source_lang: Source language code (auto-detected if None).
            formality: "default", "more", or "less".

        Returns:
            Dict with translated text, detected source language, and provider info.

        Provider: DeepL API
        Endpoint: api.deepl.com
        """
        formality_map = {
            "default": deepl.Formality.default,
            "more": deepl.Formality.more,
            "less": deepl.Formality.less,
        }

        try:
            result = self.client.translate_text(
                text,
                target_lang=target_lang.upper(),
                source_lang=source_lang.upper() if source_lang else None,
                formality=formality_map.get(formality, deepl.Formality.default),
            )

            return {
                "translated_text": result.text,
                "detected_source_lang": result.detected_source_lang.lower(),
                "target_lang": target_lang,
                "provider": "deepl",
                "endpoint": "api.deepl.com",
                "error": None,
            }

        except deepl.DeepLException as e:
            return {
                "translated_text": "",
                "detected_source_lang": "",
                "target_lang": target_lang,
                "provider": "deepl",
                "error": str(e),
            }

    def translate_batch(
        self,
        texts: List[str],
        target_lang: str,
        source_lang: Optional[str] = None,
        formality: str = "default",
    ) -> List[Dict[str, str]]:
        """
        Translate multiple image descriptions in a single batch request.

        Args:
            texts: List of image descriptions to translate.
            target_lang: Target language code.
            source_lang: Source language code (auto-detected if None).
            formality: Formality level.

        Returns:
            List of translation result dicts.
        """
        if not texts:
            return []

        formality_map = {
            "default": deepl.Formality.default,
            "more": deepl.Formality.more,
            "less": deepl.Formality.less,
        }

        try:
            results = self.client.translate_text(
                texts,
                target_lang=target_lang.upper(),
                source_lang=source_lang.upper() if source_lang else None,
                formality=formality_map.get(formality, deepl.Formality.default),
            )

            return [
                {
                    "translated_text": r.text,
                    "detected_source_lang": r.detected_source_lang.lower(),
                    "target_lang": target_lang,
                    "provider": "deepl",
                    "endpoint": "api.deepl.com",
                    "error": None,
                }
                for r in results
            ]

        except deepl.DeepLException as e:
            return [
                {
                    "translated_text": "",
                    "detected_source_lang": "",
                    "target_lang": target_lang,
                    "provider": "deepl",
                    "error": str(e),
                }
                for _ in texts
            ]


def translate_alt_text(
    description: str,
    target_language: str,
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs,
) -> Dict[str, str]:
    """
    Convenience function to translate an image alt-text description.

    Provider: DeepL API (api.deepl.com)
    """
    translator = DeepLTranslator(api_key=api_key)
    return translator.translate_description(
        text=description,
        target_lang=target_language,
        source_lang=source_language,
        **kwargs,
    )


def translate_alt_text_batch(
    descriptions: List[str],
    target_language: str,
    source_language: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs,
) -> List[Dict[str, str]]:
    """
    Convenience function to translate multiple image descriptions.

    Provider: DeepL API (api.deepl.com)
    """
    translator = DeepLTranslator(api_key=api_key)
    return translator.translate_batch(
        texts=descriptions,
        target_lang=target_language,
        source_lang=source_language,
        **kwargs,
    )


def format_translation_output(result: Dict[str, str]) -> str:
    """Format translation results for display."""
    if result.get("error"):
        return f"Error: {result['error']}"

    lines = [
        f"Source ({result.get('detected_source_lang', 'auto')}): {result.get('translated_text', '')}",
        f"Target ({result['target_lang']}): {result['translated_text']}",
        f"Provider: {result['provider']} ({result['endpoint']})",
    ]
    return "\n".join(lines)


def main():
    """CLI entry point for alt-text translation."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Translate image descriptions using DeepL API"
    )
    parser.add_argument("text", help="Image description text to translate")
    parser.add_argument("target_lang", help="Target language code (e.g., de, fr, ja)")
    parser.add_argument("--source-lang", default=None, help="Source language code")
    parser.add_argument("--formality", default="default", choices=["default", "more", "less"])
    parser.add_argument("--json", action="store_true", help="Output as JSON")

    args = parser.parse_args()

    result = translate_alt_text(
        description=args.text,
        target_language=args.target_lang,
        source_language=args.source_lang,
        formality=args.formality,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(format_translation_output(result))


if __name__ == "__main__":
    main()
