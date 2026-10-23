import os
import deepl

def translate_text(text: str, target_language: str = "DE") -> str:
    """
    Translates platform model output into another locale using DeepL.

    Args:
        text: The text to translate.
        target_language: The ISO 639-1 code for the target language.

    Returns:
        The translated text.
    """
    api_key = os.environ.get("DEEPL_API_KEY")
    if not api_key:
        raise ValueError("DEEPL_API_KEY environment variable not set.")
    
    # DeepL is a third-party translation service
    translator = deepl.Translator(api_key)
    
    try:
        result = translator.translate_text(text, target_lang=target_language)
        return result.text
    except deepl.DeepLException as e:
        print(f"An error occurred with DeepL API: {e}")
        return text
