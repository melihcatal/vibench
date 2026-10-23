import os
import deepl
from identity_models import DeepLTranslation


def translate_welcome(text: str, target_locale: str = "en") -> DeepLTranslation:
    """Translates onboarding copy into the user's locale using DeepL API.

    Returns a dict with the translated text and detected source language.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise RuntimeError("DEEPL_AUTH_KEY environment variable not set")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_locale.upper())
    return {
        "text": result.text,
        "detected_source_language": result.detected_source_language,
    }  # type: DeepLTranslation
