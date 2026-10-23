# [LATER-STEP] appeal_translate.py

from translation_client import TranslationClient
from safety_models import TextModerationResult, UnsafeSpan

CLIENT = TranslationClient()

def translate_appeal(appeal_text: str, target_lang: str = 'en') -> str:
    """Translate an appeal message for human reviewers.
    Uses the configured translation provider.
    """
    translated = CLIENT.translate(text=appeal_text, target_lang=target_lang)
    return translated.content  # assuming .content holds the translated string
