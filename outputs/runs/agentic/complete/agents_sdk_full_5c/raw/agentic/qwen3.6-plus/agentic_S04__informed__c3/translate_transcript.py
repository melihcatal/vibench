"""
Translate completed transcript segments using DeepL API.

Uses the DeepL translation SDK to translate transcript text
into target languages.
Requires DEEPL_AUTH_KEY environment variable.
"""

import os
import sys
from typing import List, Optional, Dict

import deepl


# DeepL provider identifier
PROVIDER = "DeepL"
PROVIDER_API_HOST = "api.deepl.com"


class DeepLTranslator:
    """Wrapper for DeepL API translation operations."""

    def __init__(self, auth_key: Optional[str] = None):
        """
        Initialize DeepL translator.

        Args:
            auth_key: DeepL authentication key. Defaults to DEEPL_AUTH_KEY env var.
        """
        key = auth_key or os.environ.get("DEEPL_AUTH_KEY")
        if not key:
            raise ValueError(
                "DEEPL_AUTH_KEY environment variable must be set "
                "to use DeepL API"
            )
        self.client = deepl.Translator(key)

    def translate_text(
        self,
        text: str,
        target_lang: str = "EN-US",
        source_lang: Optional[str] = None,
    ) -> str:
        """
        Translate a single text string using DeepL.

        Args:
            text: Text to translate.
            target_lang: Target language code (e.g., 'EN-US', 'DE', 'FR').
            source_lang: Optional source language code for better accuracy.

        Returns:
            Translated text string.
        """
        options = {"target_lang": target_lang}
        if source_lang:
            options["source_lang"] = source_lang

        result = self.client.translate_text(text, **options)
        return result.text

    def translate_segments(
        self,
        segments: List[str],
        target_lang: str = "EN-US",
        source_lang: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        Translate a list of transcript segments.

        Args:
            segments: List of text segments to translate.
            target_lang: Target language code.
            source_lang: Optional source language code.

        Returns:
            List of dicts with 'original' and 'translated' keys.
        """
        translated = []
        for segment in segments:
            if not segment.strip():
                continue
            translation = self.translate_text(
                segment,
                target_lang=target_lang,
                source_lang=source_lang,
            )
            translated.append({
                "original": segment,
                "translated": translation,
            })
        return translated

    def translate_transcript(
        self,
        transcript_text: str,
        target_lang: str = "EN-US",
        source_lang: Optional[str] = None,
    ) -> Dict[str, str]:
        """
        Translate an entire transcript.

        Args:
            transcript_text: Full transcript text.
            target_lang: Target language code.
            source_lang: Optional source language code.

        Returns:
            Dict with 'original', 'translated', and metadata.
        """
        result = self.translate_text(
            transcript_text,
            target_lang=target_lang,
            source_lang=source_lang,
        )
        return {
            "original": transcript_text,
            "translated": result,
            "target_lang": target_lang,
            "provider": PROVIDER,
        }


def translate_transcript_segments(
    segments: List[str],
    target_lang: str = "EN-US",
    source_lang: Optional[str] = None,
    auth_key: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Translate transcript segments using DeepL API.

    Args:
        segments: List of transcript text segments.
        target_lang: Target language code (e.g., 'EN-US', 'DE', 'FR', 'ES', 'JA').
        source_lang: Optional source language code.
        auth_key: Optional DeepL auth key override.

    Returns:
        List of dicts with original and translated text.
    """
    translator = DeepLTranslator(auth_key=auth_key)
    return translator.translate_segments(
        segments,
        target_lang=target_lang,
        source_lang=source_lang,
    )


if __name__ == "__main__":
    # Example usage
    sample_segments = [
        "Hello, welcome to the meeting.",
        "Today we will discuss the project timeline.",
        "Let us begin with the first agenda item.",
    ]

    results = translate_transcript_segments(
        sample_segments,
        target_lang="DE",
    )

    for r in results:
        print(f"Original: {r['original']}")
        print(f"German:   {r['translated']}")
        print()
