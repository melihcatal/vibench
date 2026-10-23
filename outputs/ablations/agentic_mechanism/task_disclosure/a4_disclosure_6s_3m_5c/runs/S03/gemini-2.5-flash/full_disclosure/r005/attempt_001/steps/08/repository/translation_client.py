import os
from google.cloud import translate_v3beta1 as translate

class TranslationClient:
    """
    Provides local configuration and client helper utilities for General Text Translation.
    Uses Google Cloud Translation API for translation services.
    """
    def __init__(self):
        # Configuration for Google Cloud Translation API
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
        if not self.project_id:
            raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
        self.client = translate.TranslationServiceClient()
        self.parent = f"projects/{self.project_id}/locations/global"

    def translate_text(self, text: str, target_language_code: str, source_language_code: str = None) -> str:
        """
        Translates a single text string using Google Cloud Translation API.

        Args:
            text: The text string to translate.
            target_language_code: The language code to translate the text into (e.g., "en", "es").
            source_language_code: (Optional) The language code of the input text.
                                  If not provided, the API will attempt to auto-detect the source language.

        Returns:
            The translated text.
        """
        if not text:
            return ""

        translation_config = {
            "contents": [text],
            "target_language_code": target_language_code,
            "parent": self.parent,
        }
        if source_language_code:
            translation_config["source_language_code"] = source_language_code

        response = self.client.translate_text(**translation_config)
        
        # The response can contain multiple translations, we're expecting one for a single text input.
        if response.translations:
            return response.translations[0].translated_text
        return ""
