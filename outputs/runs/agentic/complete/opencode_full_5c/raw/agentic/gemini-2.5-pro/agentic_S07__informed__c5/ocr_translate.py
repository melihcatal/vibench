import os
import deepl
from document_models import TranslationResponse


def ocr_translate(text: str, target_lang: str = "EN-US") -> TranslationResponse:
    """
    Translates extracted OCR text using DeepL.
    """
    auth_key = os.environ.get("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable not set.")

    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)

    return TranslationResponse(
        translated_text=result.text, detected_source_lang=result.detected_source_lang
    )
