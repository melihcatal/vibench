"""
Translate identity-provider consent copy using Google Cloud Translation.

Provider: Google Cloud Translation API v3
Model: google-nmt (Neural Machine Translation)
Environment variable: GOOGLE_APPLICATION_CREDENTIALS

Translates consent text, privacy notices, and identity-provider
agreement copy between languages for federated login flows.
"""

from __future__ import annotations

import os
from typing import Optional

from google.cloud import translate_v3 as translate


class ConsentTranslator:
    """Translates identity-provider consent copy using Google Cloud Translation."""

    DEFAULT_TARGET_LANGUAGE = "en"

    def __init__(
        self,
        project_id: Optional[str] = None,
        credentials_path: Optional[str] = None,
    ):
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT", "")
        self.credentials_path = credentials_path or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS", ""
        )

        client_options = None
        if self.credentials_path:
            from google.oauth2 import service_account

            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            self.client = translate.TranslationServiceClient(credentials=credentials)
        else:
            self.client = translate.TranslationServiceClient()

        self.parent = f"projects/{self.project_id}/locations/global"

    def translate_text(
        self,
        text: str,
        source_language: str,
        target_language: str = DEFAULT_TARGET_LANGUAGE,
        mime_type: str = "text/plain",
    ) -> str:
        """
        Translate consent copy from one language to another.

        Args:
            text: The consent text to translate
            source_language: BCP-47 source language code (e.g., "de", "fr", "ja")
            target_language: BCP-47 target language code (default: "en")
            mime_type: Content type ("text/plain" or "text/html")

        Returns:
            Translated text string.
        """
        if not self.project_id:
            raise ValueError(
                "Google Cloud project ID is required. "
                "Set GOOGLE_CLOUD_PROJECT or pass project_id."
            )

        response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": [text],
                "mime_type": mime_type,
                "source_language_code": source_language,
                "target_language_code": target_language,
            }
        )

        if response.translations:
            return response.translations[0].translated_text
        return text

    def translate_batch(
        self,
        texts: list[str],
        source_language: str,
        target_language: str = DEFAULT_TARGET_LANGUAGE,
    ) -> list[str]:
        """
        Translate multiple consent texts in a single batch request.

        Returns a list of translated strings.
        """
        if not self.project_id:
            raise ValueError(
                "Google Cloud project ID is required. "
                "Set GOOGLE_CLOUD_PROJECT or pass project_id."
            )

        response = self.client.translate_text(
            request={
                "parent": self.parent,
                "contents": texts,
                "mime_type": "text/plain",
                "source_language_code": source_language,
                "target_language_code": target_language,
            }
        )

        return [t.translated_text for t in response.translations]

    def translate_consent_document(
        self,
        consent_text: str,
        target_languages: list[str],
        source_language: str = "en",
    ) -> dict[str, str]:
        """
        Translate consent copy into multiple target languages.

        Returns a dict mapping language codes to translated text.
        """
        translations = {}
        for lang in target_languages:
            translated = self.translate_text(
                text=consent_text,
                source_language=source_language,
                target_language=lang,
            )
            translations[lang] = translated
        return translations


def translate_consent_copy(
    text: str,
    source_language: str,
    target_language: str = "en",
    project_id: Optional[str] = None,
) -> str:
    """
    Convenience function to translate consent copy using Google Cloud Translation.

    Returns the translated text string.
    """
    translator = ConsentTranslator(project_id=project_id)
    return translator.translate_text(
        text=text,
        source_language=source_language,
        target_language=target_language,
    )


def translate_consent_batch(
    texts: list[str],
    source_language: str,
    target_language: str = "en",
    project_id: Optional[str] = None,
) -> list[str]:
    """
    Convenience function to batch-translate consent copy.

    Returns a list of translated strings.
    """
    translator = ConsentTranslator(project_id=project_id)
    return translator.translate_batch(
        texts=texts,
        source_language=source_language,
        target_language=target_language,
    )


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print(
            "Usage: python consent_translate.py <text> <source_lang> [target_lang]"
        )
        sys.exit(1)

    text = sys.argv[1]
    src = sys.argv[2]
    tgt = sys.argv[3] if len(sys.argv) > 3 else "en"

    translated = translate_consent_copy(text, source_language=src, target_language=tgt)
    print(f"Translated: {translated}")
