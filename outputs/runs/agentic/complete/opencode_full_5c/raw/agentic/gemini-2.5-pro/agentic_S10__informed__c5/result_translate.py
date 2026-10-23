import os
from dotenv import load_dotenv
import deepl

load_dotenv()


def translate_text_deepl(text: str, target_language: str = "DE"):
    """
    Translates generated model output using the DeepL API.
    """
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY not found in environment variables.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_language)
    return result.text
