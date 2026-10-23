# translation_client.py
import os
import json
from typing import Dict, Any

# Placeholder for configuration – in real usage, load from env or config file
# For this example we use DeepL as the concrete external translation provider.
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")
DEEPL_URL = "https://api.deepl.com/v2/translate"


class TranslationClient:
    """Local helper utilities for General Text Translation with DeepL."""

    @staticmethod
    def translate_text(source_text: str, target_lang: str = "EN") -> str:
        """Translate a single text string using DeepL."""
        payload = {
            "auth_key": DEEPL_API_KEY,
            "text": source_text,
            "target_lang": target_lang,
        }
        response = TranslationClient._call_api(payload)
        return response.get("text", source_text)

    @staticmethod
    def translate_batch(texts: list[str], target_lang: str = "EN") -> list[str]:
        """Translate a list of strings while preserving order."""
        results = []
        for text in texts:
            results.append(TranslationClient.translate_text(text, target_lang))
        return results

    @staticmethod
    def translate_markup(source_html: str, target_lang: str = "EN") -> str:
        """Translate HTML while preserving tags."""
        # DeepL supports HTML input via the "html" flag.
        payload = {
            "auth_key": DEEPL_API_KEY,
            "text": source_html,
            "target_lang": target_lang,
            "html": True,
        }
        response = TranslationClient._call_api(payload)
        return response.get("text", source_html)

    @staticmethod
    def translate_dictionary_values(
        data: Dict[str, str], target_lang: str = "EN"
    ) -> Dict[str, str]:
        """Translate values in a dict, preserving keys."""
        return {
            k: TranslationClient.translate_text(v, target_lang) for k, v in data.items()
        }

    @staticmethod
    def _call_api(payload: dict) -> dict:
        import requests

        resp = requests.post(DEEPL_URL, data=payload, timeout=10)
        resp.raise_for_status()
        return resp.json()


# Utility to load provider specific settings from env or file
def load_config() -> dict:
    return {
        "api_key": DEEPL_API_KEY,
        "endpoint": DEEPL_URL,
    }
