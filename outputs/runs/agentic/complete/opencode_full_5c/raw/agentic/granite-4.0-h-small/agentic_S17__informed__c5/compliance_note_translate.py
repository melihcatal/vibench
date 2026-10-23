# compliance_note_translate.py
# Translate encryption or compliance notes for reviewers using Azure AI Translator

import os
import requests
from urllib.parse import quote_plus

# Provider: Azure AI Translator (REST endpoint)
# Expected env vars: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION

AZURE_TRANSLATOR_KEY = os.getenv("AZURE_TRANSLATOR_KEY")
AZURE_TRANSLATOR_REGION = os.getenv("AZURE_TRANSLATOR_REGION")
if not AZURE_TRANSLATOR_KEY or not AZURE_TRANSLATOR_REGION:
    raise RuntimeError(
        "Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables"
    )

TRANSLATOR_ENDPOINT = f"https://{AZURE_TRANSLATOR_REGION}.api.cognitive.microsofttranslator.com/translate?api-version=3.0"

SUPPORTED_TARGETS = ["es", "fr", "de", "ja", "zh-Hans", "pt"]


def translate_note(note: str, target_lang: str = "es") -> dict:
    """Translate a compliance note to the target language code.\n    Returns the raw JSON response from Azure Translator API.\n    Raises RuntimeError for any error (including unsupported target)."""
    if target_lang not in SUPPORTED_TARGETS:
        raise RuntimeError(
            f"Unsupported target language '{target_lang}'. Supported: {SUPPORTED_TARGETS}"
        )
    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Trace": "true",
    }
    body = [{"Text": note}]
    params = {"to": target_lang}
    resp = requests.post(TRANSLATOR_ENDPOINT, headers=headers, json=body, params=params)
    resp.raise_for_status()
    return resp.json()


if __name__ == "__main__":
    sample = "Encryption key 'data-key-001' was rotated on 2025-07-01."
    translation = translate_note(sample, target_lang="fr")
    print("Translated note:", translation)
