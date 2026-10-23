import os
import deepl
from model_models import TranslationResult
from dotenv import load_dotenv

load_dotenv()


def translate_text(text: str, target_lang: str = "en") -> TranslationResult:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)

    return TranslationResult(
        translated_text=result.text, detected_source_lang=result.detected_source_lang
    )
