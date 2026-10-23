# LATER-STEP: Translate user appeal text for reviewers

from safety_client import get_client
import google.cloud.translate_v2 as translate  # Concrete provider: Google Translate


def translate_appeal(appeal_text: str, target_lang: str = "en") -> str:
    """Translate appeal text to English for easier reviewer handling."""
    client = get_client()
    translate_client = translate.Client()
    translated = translate_client.translate(appeal_text, target_language=target_lang)
    return translated["translatedText"]
