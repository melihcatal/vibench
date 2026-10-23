import os
import json
from typing import Dict, Any
from google.cloud import translate_v2 as translate

# Google Cloud Translation client (uses env var GOOGLE_APPLICATION_CREDENTIALS)
translate_client = translate.Client()

# Mapping of source language to target languages for consent UI
TRANSLATIONS = {
    # Consent copy stored per Identity Provider (e.g., Auth0, Google, Azure)
    # Example: key is the provider slug, value is the source language of the original copy
    'auth0': 'en',
    'google_idp': 'en',
    'azure_ad': 'en',
}

# Destination languages list – can be expanded
TARGET_LANGS = ['es', 'fr', 'de', 'ja', 'zh']


def translate_consent(provider: str, consent_text: str) -> Dict[str, Any]:
    """
    Translate a provider's consent text into multiple target languages.
    Returns a dict mapping language code -> translated text.
    """
    results = {}
    if provider not in TRANSLATIONS:
        raise ValueError(f'Unsupported provider: {provider}')
    src_lang = TRANSLATIONS[provider]
    for target in TARGET_LANGS:
        if src_lang == target:
            continue  # skip self-translation
        try:
            resp = translate_client.translate(consent_text, target_language=target, source_language=src_lang)
            results[target] = resp['translatedText']
        except Exception as e:
            # Log and continue with partial results
            print(f'Translation error for {provider} ({src_lang} -> {target}): {e}')
    return results

# ---------------------------------------------------------------------------
# CLI example (replace with service integration as needed)
# ---------------------------------------------------------------------------
if __name__ == '__main__':
    # Demo: translate a mock consent block
    demo_copy = (
        "By clicking 'Allow', you consent to the collection and processing of your
        personal data for authentication purposes."
    )
    provider = 'auth0'
    translations = translate_consent(provider, demo_copy)
    print(json.dumps({provider: translations}, indent=2))
