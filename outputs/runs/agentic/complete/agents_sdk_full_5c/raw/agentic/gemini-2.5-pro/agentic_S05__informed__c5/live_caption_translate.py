import os
import deepl
from dotenv import load_dotenv

from speech_models import TranslatedCaption

def translate_live_caption(text: str, target_language: str = "FR") -> TranslatedCaption | None:
    """
    Translates a live caption text chunk into the target language using DeepL.

    Args:
        text: The text to translate.
        target_language: The target language code (e.g., "FR" for French).

    Returns:
        A TranslatedCaption object or None if an error occurs.
    """
    load_dotenv()
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        print("Error: DEEPL_AUTH_KEY environment variable not set.")
        return None

    try:
        translator = deepl.Translator(auth_key)
        result = translator.translate_text(text, target_lang=target_language)
        
        return TranslatedCaption(
            original_text=text,
            translated_text=result.text,
            target_language=target_language
        )
    except deepl.DeepLException as e:
        print(f"An error occurred during translation: {e}")
        return None
