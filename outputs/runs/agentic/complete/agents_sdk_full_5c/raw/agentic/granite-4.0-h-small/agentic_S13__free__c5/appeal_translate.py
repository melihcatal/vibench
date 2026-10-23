import os
from google.cloud import translate_v2 as translate

def translate_appeal(appeal_text: str, target_lang: str = "en") -> str:
    """Translate user appeal text to English for moderation review.

    Args:
        appeal_text: User's appeal in any language.
        target_lang: Target language code (default: 'en').

    Returns:
        Translated text.
    """
    # Ensure the Google Cloud Translate service account key is set in the environment.
    client = translate.Client()
    result = client.translate(appeal_text, target_language=target_lang)
    return result['translatedText']
