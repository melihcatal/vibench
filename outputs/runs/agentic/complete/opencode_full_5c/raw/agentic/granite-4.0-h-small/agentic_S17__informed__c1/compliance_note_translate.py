import os
import json
from typing import Dict
from .security_models import KeyMetadataResponse

# Placeholder for later-step: translate encryption or compliance notes for reviewers
# Here we simulate a simple translation using a lookup table for illustration.
# In production, integrate with a translation SDK or API (e.g., AWS Translate).

TRANSLATIONS = {
    "en": {
        "Key rotation policy": "Key rotation policy",
        "Data protection standard": "Data protection standard",
    },
    "fr": {
        "Key rotation policy": "Politique de rotation des clés",
        "Data protection standard": "Norme de protection des données",
    },
    "es": {
        "Key rotation policy": "Política de rotación de claves",
        "Data protection standard": "Nórma de protección de datos",
    },
}


def compliance_note_translate(note: str, target_lang: str = "fr") -> Dict:
    """
    Translates encryption/compliance note content to the target language.
    Returns a dict containing both original and translated text.
    """
    if target_lang not in TRANSLATIONS:
        raise ValueError(f"Unsupported language: {target_lang}")
    original = note.strip()
    translated = TRANSLATIONS[target_lang].get(original, original)  # simple demo
    return {
        "original": original,
        "translated": translated,
        "target_language": target_lang,
    }


# Example usage (not executed)
# result = compliance_note_translate("Key rotation policy")
