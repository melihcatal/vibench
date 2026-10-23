import os
import deepl


def translate_script(text: str, target_lang: str = "FR") -> str:
    """
    Translates a script to the target language using the DeepL API.

    Requires the DEEPL_AUTH_KEY environment variable to be set.

    Args:
        text: The text to translate.
        target_lang: The target language code (e.g., "FR" for French, "ES" for Spanish).

    Returns:
        The translated text.
        
    Raises:
        ValueError: If the DEEPL_AUTH_KEY is not set.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        print(f"An error occurred during translation: {e}")
        raise
