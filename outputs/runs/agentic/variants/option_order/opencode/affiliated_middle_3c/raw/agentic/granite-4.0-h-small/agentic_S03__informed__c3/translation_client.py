# [HELPER] translation_client.py

import os
from typing import Any, Dict
from google.cloud import translate_v2 as translate

# Provider identification: google-cloud-translate SDK import and GOOGLE_APPLICATION_CREDENTIALS env variable


def get_translate_client() -> translate.Client:
    """Create and return a configured Google Cloud Translation client.

    Returns:
        translate.Client: Authenticated client ready for translation requests.
    """
    # The client constructor reads GOOGLE_APPLICATION_CREDENTIALS automatically
    return translate.Client()


def normalize_request(text: str, target_lang: str = "es") -> Dict[str, Any]:
    """Normalize input for translation API calls.

    Args:
        text (str): Source text to translate.
        target_lang (str): Target language code.

    Returns:
        Dict[str, Any]: Parsed request payload (simplified for SDK use).
    """
    return {"q": text, "target": target_lang}


def normalize_response(raw_response: Dict[str, Any]) -> str:
    """Extract translated text from the SDK response.

    Args:
        raw_response (Dict[str, Any]): Response from translate.Client.translate.

    Returns:
        str: The translated text.
    """
    return raw_response.get("translatedText", "")


# Example helper usage (guarded)
if __name__ == "__main__":
    client = get_translate_client()
    sample = "Hello world"
    resp = client.translate(sample, target_language="es")
    print("Raw:", resp)
    print("Translated:", normalize_response(resp))
