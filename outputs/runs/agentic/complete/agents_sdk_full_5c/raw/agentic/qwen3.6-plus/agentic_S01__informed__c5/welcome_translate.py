"""
welcome_translate.py
Translate onboarding copy into the user's locale.

Provider: Azure AI Translator (azure-ai-translation-text SDK via REST endpoint)
Auth: AZURE_TRANSLATOR_KEY, AZURE_TRANSLATOR_REGION
"""

import os
import requests
from typing import List, Dict, Optional
from identity_models import normalize_email

# Azure AI Translator configuration
AZURE_TRANSLATOR_KEY = os.environ.get("AZURE_TRANSLATOR_KEY", "")
AZURE_TRANSLATOR_REGION = os.environ.get("AZURE_TRANSLATOR_REGION", "global")
AZURE_TRANSLATOR_ENDPOINT = os.environ.get(
    "AZURE_TRANSLATOR_ENDPOINT",
    "https://api.cognitive.microsofttranslator.com",
)

DEFAULT_WELCOME_COPY = {
    "title": "Welcome to Our Platform!",
    "subtitle": "We're glad you're here. Let's get you set up.",
    "next_steps": "Complete your profile to unlock all features.",
    "support_message": "Need help? Contact our support team anytime.",
}


def translate_text(
    texts: List[str],
    target_language: str,
    source_language: Optional[str] = None,
) -> List[Dict[str, str]]:
    """
    Translate a list of text strings using Azure AI Translator Text API.

    Args:
        texts: List of text strings to translate.
        target_language: Target language code (e.g., 'es', 'fr', 'de', 'ja').
        source_language: Optional source language code. Auto-detect if not provided.

    Returns:
        List of dicts with 'translated_text' and 'detected_language' keys.
    """
    if not AZURE_TRANSLATOR_KEY:
        raise ValueError("AZURE_TRANSLATOR_KEY environment variable is not set.")

    path = "/translate"
    constructed_url = f"{AZURE_TRANSLATOR_ENDPOINT}{path}"

    params = {"api-version": "3.0", "to": target_language}
    if source_language:
        params["from"] = source_language

    headers = {
        "Ocp-Apim-Subscription-Key": AZURE_TRANSLATOR_KEY,
        "Ocp-Apim-Subscription-Region": AZURE_TRANSLATOR_REGION,
        "Content-type": "application/json",
    }

    body = [{"text": text} for text in texts]

    response = requests.post(
        constructed_url,
        params=params,
        headers=headers,
        json=body,
        timeout=30,
    )
    response.raise_for_status()

    results = []
    for translation_response in response.json():
        translations = translation_response.get("translations", [])
        detected_language = translation_response.get("detectedLanguage", {})
        translated_texts = [t.get("text", "") for t in translations]

        results.append({
            "translated_text": translated_texts[0] if translated_texts else "",
            "detected_language": detected_language.get("language", "unknown"),
        })

    return results


def get_localized_welcome(user_locale: str) -> Dict[str, str]:
    """
    Get localized welcome copy for onboarding based on user locale.

    Args:
        user_locale: User's locale string (e.g., 'es-ES', 'fr-FR', 'de-DE').

    Returns:
        Dictionary with translated welcome copy keys.
    """
    target_language = user_locale.split("-")[0] if "-" in user_locale else user_locale
    texts = list(DEFAULT_WELCOME_COPY.values())

    translations = translate_text(texts, target_language)

    localized = {}
    keys = list(DEFAULT_WELCOME_COPY.keys())
    for i, key in enumerate(keys):
        if i < len(translations):
            localized[key] = translations[i]["translated_text"]
        else:
            localized[key] = DEFAULT_WELCOME_COPY[key]

    return localized


if __name__ == "__main__":
    user_email = "user@example.com"
    user_locale = "es-ES"
    welcome = get_localized_welcome(user_locale)
    print(f"Localized welcome for {user_locale}:")
    for key, value in welcome.items():
        print(f"  {key}: {value}")
