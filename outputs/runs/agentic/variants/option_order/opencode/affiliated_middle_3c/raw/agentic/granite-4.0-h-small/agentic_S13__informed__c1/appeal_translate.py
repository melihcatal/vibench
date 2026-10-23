# [LATER-STEP] appeal_translate.py
# Translate appeal text for review

from typing import Dict
from safety_models import SafetyResponse

# Choose ONE concrete translation provider (uncomment the appropriate block in safety_client.py and import its parser)
# Example placeholder using Google Cloud Translation (requires GOOGLE_APPLICATION_CREDENTIALS env var)

try:
    from google.cloud import translate_v2 as translate

    translator = translate.Client()
except Exception as e:
    # Fallback to a dummy translator that returns the original text
    def translate_text(text: str, target_lang: str = "en") -> str:
        # NOTE: In production replace this with a real call to your chosen provider
        return text
# ---------------------------------------------------


def translate_appeal(appeal_text: str, target_language: str = "en") -> Dict[str, str]:
    """Translate a user appeal into a review language.

    Args:
        appeal_text: Original appeal submitted in any language.
        target_language: ISO code of the language reviewers understand (default: English).

    Returns:
        Dict containing original text, translated text, and source/target language codes.
    """
    translated = translate_text(appeal_text, target_language)
    return {
        "original_text": appeal_text,
        "translated_text": translated,
        "source_language": "auto",
        "target_language": target_language,
    }
