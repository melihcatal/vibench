import os
import deepl

from security_models import TranslationRequest


def translate_compliance_note(request: TranslationRequest) -> str:
    """
    Translates a compliance or encryption note to a specified language.

    Args:
        request: A TranslationRequest with the text and target language.

    Returns:
        The translated text as a string.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(
            request.text, target_lang=request.target_lang
        )
        return result.text
    except deepl.exceptions.DeepLException as e:
        print(f"An error occurred with the DeepL API: {e}")
        raise
