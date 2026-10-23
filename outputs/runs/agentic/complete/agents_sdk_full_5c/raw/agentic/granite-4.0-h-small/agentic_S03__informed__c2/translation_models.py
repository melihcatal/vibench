import os
from typing import Dict, Any, List
from google.cloud.translate_v2 import Translator

class TranslationModels:
    """Helper utilities for request/response normalization and post‑processing."""
    @staticmethod
def normalize_response(response: Dict[str, Any]) -> Dict[str, str]:
        """Extract the translated text from a provider response.
        The Google Translate API returns a dict with a key 'translatedText'.
        This method standardizes the output for downstream components."
        return response.get('translatedText', '')
    
    @staticmethod
def normalize_batch_response(batch: List[Dict[str, Any]]) -> List[str]:
        """
        Extract translated text from a batch response list.
        Each element is expected to contain a 'translatedText' field.
        """
        return [item.get('translatedText', '') for item in batch]
    
    @staticmethod
def flatten_nested(data: Any) -> List[str]:
        """Recursively walk nested dicts/lists and return all string leaves.
        Useful for extracting text from complex payloads before translation."""
        strings = []
        if isinstance(data, str):
            strings.append(data)
        elif isinstance(data, dict):
            for value in data.values():
                strings.extend(TranslationModels.flatten_nested(value))
        elif isinstance(data, list):
            for elem in data:
                strings.extend(TranslationModels.flatten_nested(elem))
        return strings

    @staticmethod
def reassemble_translated(original: str, translation: str) -> str:
        """
        Very simple placeholder that returns the translation.
        In a real‑world scenario you might re‑inject placeholders or markup.
        """
        return translation

    # Dummy stubs for provider‑agnostic signatures that downstream steps can import
    def translate_single(self, text: str, target_lang: str) -> Dict[str, str]:
        """Stub matching the interface expected by same‑scenario files."""
        client = Translator()
        resp = client.translate(text, target_language=target_lang)
        return {'translatedText': resp['translatedText']}
    
    def translate_batch(self, texts: List[str], target_lang: str) -> List[Dict[str, str]]:
        client = Translator()
        resp = client.translate(texts, target_language=target_lang)
        return [{'translatedText': item['translatedText']} for item in resp]

# Simple test harness (remove for production library)
if __name__ == "__main__":
    tm = TranslationModels()
    print(tm.normalize_response({'translatedText': 'Bonjour le monde'}))
