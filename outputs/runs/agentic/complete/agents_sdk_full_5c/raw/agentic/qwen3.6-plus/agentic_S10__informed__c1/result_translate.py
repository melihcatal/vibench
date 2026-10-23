"""
Translate generated model output using DeepL API.
Provider: DeepL Translation API
SDK: requests (REST API)
Auth: DEEPL_AUTH_KEY
"""

import os
import requests
from typing import Optional, List, Dict, Any


# Provider-specific environment variables
DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_API_URL = "https://api.deepl.com/v2/translate"
DEEPL_FREE_API_URL = "https://api-free.deepl.com/v2/translate"


class DeepLTranslator:
    """Client for DeepL Translation API."""

    def __init__(
        self,
        auth_key: Optional[str] = None,
        use_free_api: bool = False,
    ):
        self.auth_key = auth_key or DEEPL_AUTH_KEY
        self.api_url = DEEPL_FREE_API_URL if use_free_api else DEEPL_API_URL

    def translate_text(
        self,
        text: str,
        target_lang: str = "EN",
        source_lang: Optional[str] = None,
        formality: Optional[str] = None,
    ) -> str:
        """
        Translate text using the DeepL API.

        Args:
            text: The text to translate.
            target_lang: Target language code (e.g., "EN", "DE", "FR", "ES", "JA").
            source_lang: Optional source language code. Auto-detected if None.
            formality: Optional formality level ("more", "less", "default").

        Returns:
            Translated text string.
        """
        params = {
            "auth_key": self.auth_key,
            "text": text,
            "target_lang": target_lang.upper(),
        }
        if source_lang:
            params["source_lang"] = source_lang.upper()
        if formality:
            params["formality"] = formality

        response = requests.post(self.api_url, data=params)
        response.raise_for_status()
        result = response.json()
        translations = result.get("translations", [])
        if translations:
            return translations[0].get("text", "")
        return ""

    def translate_batch(
        self,
        texts: List[str],
        target_lang: str = "EN",
        source_lang: Optional[str] = None,
    ) -> List[str]:
        """
        Translate multiple texts using the DeepL API.

        Args:
            texts: List of texts to translate.
            target_lang: Target language code.
            source_lang: Optional source language code.

        Returns:
            List of translated text strings.
        """
        params = {
            "auth_key": self.auth_key,
            "target_lang": target_lang.upper(),
        }
        if source_lang:
            params["source_lang"] = source_lang.upper()
        for text in texts:
            params["text"] = text

        response = requests.post(self.api_url, data=params)
        response.raise_for_status()
        result = response.json()
        return [t.get("text", "") for t in result.get("translations", [])]

    def detect_language(self, text: str) -> Dict[str, Any]:
        """
        Detect the language of the given text using DeepL.

        Args:
            text: The text to detect language for.

        Returns:
            Dictionary with detected language code and confidence.
        """
        url = self.api_url.replace("/translate", "") + "/v2/language"
        params = {
            "auth_key": self.auth_key,
            "text": text,
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        result = response.json()
        if result:
            return result[0]
        return {"language": "unknown", "confidence": 0.0}


def translate_result(
    text: str,
    target_lang: str = "EN",
    source_lang: Optional[str] = None,
) -> str:
    """
    Quick function to translate text using DeepL.

    Args:
        text: The text to translate.
        target_lang: Target language code.
        source_lang: Optional source language code.

    Returns:
        Translated text string.
    """
    translator = DeepLTranslator()
    return translator.translate_text(text, target_lang, source_lang)


if __name__ == "__main__":
    if not DEEPL_AUTH_KEY:
        print("DEEPL_AUTH_KEY environment variable is required.")
    else:
        translator = DeepLTranslator()
        test_text = "Bonjour le monde, comment allez-vous aujourd'hui?"
        result = translator.translate_text(test_text, target_lang="EN")
        print(f"Original: {test_text}")
        print(f"Translation: {result}")
