from typing import Literal

from safety_client import get_deepl_translator

TargetLanguage = Literal["EN-US", "DE", "FR", "ES", "JA"]

def translate_appeal(text: str, target_lang: TargetLanguage = "EN-US") -> str:
    """
    Translates appeal text for review using the DeepL API.
    """
    translator = get_deepl_translator()
    if not translator:
        raise ConnectionError("DeepL client not configured. Check DEEPL_API_KEY.")

    try:
        result = translator.translate_text(text, target_lang=target_lang)
        return result.text
    except Exception as e:
        return f"Error during translation: {e}"
