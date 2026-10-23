import os
import deepl

def translate_text(text: str, target_language_code: str = "FR") -> str:
    """
    Translates text to a target language using the DeepL API.

    Args:
        text: The text to translate.
        target_language_code: The ISO 639-1 code for the target language.
                              Defaults to "FR" (French).

    Returns:
        The translated text.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    # Provider-specific SDK client: deepl.Translator
    translator = deepl.Translator(auth_key)

    result = translator.translate_text(text, target_lang=target_language_code)
    
    return result.text
