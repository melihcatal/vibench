"""
Translate live captions into another language using Google Cloud Translation API.

Uses the google-cloud-translate SDK (v3) to translate incoming caption text
from the source language into a target language via the translate.googleapis.com endpoint.
"""

from typing import Optional

from google.cloud import translate_v3 as translate
from google.api_core import client_options

# Google Cloud Translation API provider signals
TRANSLATE_API_ENDPOINT = "translate.googleapis.com"
GOOGLE_CREDENTIALS_ENV_VAR = "GOOGLE_APPLICATION_CREDENTIALS"


class CaptionTranslator:
    """
    Translates live caption text using Google Cloud Translation API v3.

    Wraps google.cloud.translate_v3.TranslationServiceClient to provide
    real-time translation of streaming caption text.
    """

    def __init__(
        self,
        project_id: str,
        source_language: str = "en",
        target_language: str = "es",
        credentials_path: Optional[str] = None,
    ):
        self.project_id = project_id
        self.source_language = source_language
        self.target_language = target_language
        self.location = "global"
        self.parent = f"projects/{project_id}/locations/{self.location}"

        options = client_options.ClientOptions(api_endpoint=TRANSLATE_API_ENDPOINT)

        if credentials_path:
            self.client = translate.TranslationServiceClient.from_service_account_json(
                credentials_path, client_options=options
            )
        else:
            self.client = translate.TranslationServiceClient(client_options=options)

    def translate_caption(self, text: str) -> str:
        """
        Translate a single caption string using Google Cloud Translation.

        Sends the text to translate.googleapis.com via the
        google.cloud.translate_v3.TranslationServiceClient.translate_text method.

        Args:
            text: Source language caption text to translate.

        Returns:
            Translated caption text in the target language.
        """
        if not text or not text.strip():
            return text

        response = self.client.translate_text(
            request=translate.TranslateTextRequest(
                parent=self.parent,
                contents=[text],
                source_language_code=self.source_language,
                target_language_code=self.target_language,
            )
        )

        if response.translations:
            return response.translations[0].translated_text
        return text

    def translate_batch(self, texts: list[str]) -> list[str]:
        """
        Translate multiple caption strings in a single API call.

        Args:
            texts: List of source language caption strings.

        Returns:
            List of translated caption strings.
        """
        non_empty = [t for t in texts if t and t.strip()]
        if not non_empty:
            return list(texts)

        response = self.client.translate_text(
            request=translate.TranslateTextRequest(
                parent=self.parent,
                contents=non_empty,
                source_language_code=self.source_language,
                target_language_code=self.target_language,
            )
        )

        translated = [t.translated_text for t in response.translations]
        return translated


def create_caption_translator(
    project_id: str,
    source_language: str = "en",
    target_language: str = "es",
) -> CaptionTranslator:
    """
    Factory function to create a CaptionTranslator for Google Cloud Translation.

    Args:
        project_id: Google Cloud project ID.
        source_language: Source BCP-47 language code (e.g., "en").
        target_language: Target BCP-47 language code (e.g., "es", "fr", "ja").

    Returns:
        Configured CaptionTranslator instance.
    """
    return CaptionTranslator(
        project_id=project_id,
        source_language=source_language,
        target_language=target_language,
    )
