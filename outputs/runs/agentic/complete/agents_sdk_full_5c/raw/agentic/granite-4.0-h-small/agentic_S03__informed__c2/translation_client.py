import os
from typing import List, Dict, Any
from google.cloud import translate_v2 as translate

class TranslationClient:
    """Thin wrapper around Google Cloud Translation API with helper utilities."""
    def __init__(self):
        # Automatically pick up credentials from GOOGLE_APPLICATION_CREDENTIALS env var
        self.client = translate.Client()
        # Define a set of supported ISO 639-1 language codes (subset)
        self.supported_languages = {
            "en", "es", "fr", "de", "zh", "ja", "pt", "ru", "it", "nl"
        }
    
    def translate(self, text: str, target_lang: str) -> Dict[str, Any]:
        """Translate a single string using the Google Cloud Translation API."""
        result = self.client.translate(text, target_language=target_lang)
        # The API returns a dict; ensure presence of translatedText
        return result
    
    def translate_batch(self, texts: List[str], target_lang: str) -> List[Dict[str, Any]]:
        """Translate a list of strings using batch mode, preserving order."""
        # Google client can translate multiple texts at once by passing a list to client.translate.
        results = self.client.translate(texts, target_language=target_lang)
        # The result is a list of dicts when multiple texts are provided.
        return results

    def detect_language(self, text: str) -> str:
        """Detect the source language of a text string."""
        detected = self.client.detect_language(text)
        # Detected language is under 'language' key
        return detected.get('language', 'unknown')

    def get_languages(self) -> List[str]:
        """Return the list of supported language codes."""
        # Google API provides a method to list languages; we expose a static subset for simplicity.
        # Internally you could call self.client.get_languages() if needed.
        return list(self.supported_languages)

    def is_supported(self, lang_code: str) -> bool:
        """Check if a language code is supported by this client."""
        return lang_code in self.supported_languages

# Example usage (remove in library mode)
if __name__ == "__main__":
    client = TranslationClient()
    print(client.translate("Hello world", "fr"))
