import os
import deepl
from safety_models import TranslationResult


def translate_appeal(text: str, target_lang: str = "EN-US") -> TranslationResult:
    """
    Translates appeal text for review using the DeepL API.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        translated_text = result.text
    except deepl.DeepLException as e:
        return TranslationResult(
            original_text=text,
            translated_text=f"Translation failed: {e}",
            target_language=target_lang,
        )

    return TranslationResult(
        original_text=text,
        translated_text=translated_text,
        target_language=target_lang,
    )
