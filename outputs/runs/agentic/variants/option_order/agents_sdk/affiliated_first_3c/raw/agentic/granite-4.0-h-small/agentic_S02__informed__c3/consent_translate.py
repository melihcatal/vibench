from __future__ import annotations
import os
from typing import Optional
from google.cloud import translate_v2 as translate
from identity_models import TranslatedConsent

def translate_consent(consent_text: str, target_lang: str = "es") -> TranslatedConsent:
    """
    Uses Google Cloud Translation to translate identity‑provider consent text.
    Returns a TranslatedConsent object.
    """
    # The client uses the env var GOOGLE_APPLICATION_CREDENTIALS automatically.
    translator = translate.Client()
    result = translator.translate(consent_text, target_language=target_lang)
    return TranslatedConsent(
        consent_text=consent_text,
        translated_text=result["translatedText"],
        source_lang=result.get("source"),
        target_lang=target_lang
    )

if __name__ == "__main__":
    sample = "I agree to share my email address and name with the service."
    translated = translate_consent(sample, target_lang="fr")
    print("Translation result:", translated.dict())
