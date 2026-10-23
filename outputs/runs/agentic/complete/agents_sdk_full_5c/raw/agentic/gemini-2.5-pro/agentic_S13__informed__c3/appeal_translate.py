import os
import deepl
from safety_models import TranslationResult

def translate_appeal_text(
    text: str,
    target_lang: str = "EN-US"
) -> TranslationResult:
    """
    Translates appeal text to a target language for review using DeepL.

    :param text: The appeal text to be translated.
    :param target_lang: The target language code (e.g., "EN-US", "DE").
    :return: A TranslationResult object with translation details.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        
        return TranslationResult(
            original_text=text,
            translated_text=result.text,
            detected_source_lang=result.detected_source_lang
        )
    except deepl.DeepLException as e:
        # Handle API errors
        return TranslationResult(
            original_text=text,
            translated_text=f"Translation failed: {e}",
            detected_source_lang="error"
        )
