import os
import deepl

def translate_caption(text: str, target_lang: str = "FR") -> str:
    """
    Translates a caption text to the target language using DeepL.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR" for French).

    Returns:
        The translated text, or an error message.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        return "Error: DEEPL_AUTH_KEY not set."

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        if result is None:
            return "Error: No translation returned."
        return result.text
    except deepl.DeepLException as e:
        return f"Error during translation: {e}"
