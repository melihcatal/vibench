# [HELPER] translation_models.py

# Request, response, and normalization helpers for General Text Translation
from typing import Any, Dict, List

# Example request payload structure for the selected provider (DeepL SDK)


def build_translate_request(
    source_text: str, source_lang: str, target_lang: str
) -> Dict[str, Any]:
    """Create a request dictionary for DeepL translate_text.","""
    return {
        "text": source_text,
        "source_lang": source_lang,
        "target_lang": target_lang,
    }


# Example response normalization


def normalize_translate_response(provider_response: Any) -> str:
    """Extract translated text from DeepL response format.","""
    # DeepL SDK returns a dict with 'text' key
    if isinstance(provider_response, dict) and "text" in provider_response:
        return provider_response["text"]
    # Fallback for generic response types
    return str(provider_response)


# Utility to split long texts for batch translation (optional)


def chunkify(text: str, max_chars: int = 4000) -> List[str]:
    """Split text into chunks respecting provider limits (DeepL ~4000 characters)."""
    return [text[i : i + max_chars] for i in range(0, len(text), max_chars)]
