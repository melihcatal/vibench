import os
import deepl

def translate_script(text: str, target_lang: str) -> str:
    """
    Translates a script to the target language using the DeepL API.

    Args:
        text: The source text to translate.
        target_lang: The target language code (e.g., "EN-US", "DE", "FR").

    Returns:
        The translated text.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    
    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except deepl.DeepLException as e:
        print(f"Error during translation with DeepL: {e}")
        raise
