# [LATER-STEP] compliance_note_translate.py

import os
from google.cloud import translate_v2 as translate

# Concrete Google Cloud Translation client using the official SDK.

def translate_audit_note(note: str, target_lang: str = "es") -> str:
    """Translate a compliance or encryption audit note to the target language.

    Uses Google Cloud Translation API (v2) via the SDK. The function respects the
    GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication.

    Args:
        note (str): The original English audit note.
        target_lang (str): ISO 639‑1 language code (default: 'es' for Spanish).

    Returns:
        str: Translated note.
    """
    client = translate.Client()
    # Detect source language automatically; you can also pass source="en" if preferred.
    result = client.translate(note, target_language=target_lang)
    return result["translatedText"]


if __name__ == "__main__":
    # Demo: translate a sample compliance note.
    compliance_note = (
        "The encryption key was rotated on 2025‑08‑15 and complies with GDPR and CCPA requirements."
    )
    translated = translate_audit_note(compliance_note, target_lang="fr")
    print("Original note:", compliance_note)
    print("French translation:", translated)
