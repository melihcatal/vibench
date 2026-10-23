import os
import deepl
from document_models import TranslateResponse


def ocr_translate(text: str, target_lang: str = "ES") -> TranslateResponse:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(text, target_lang=target_lang)
    return {"translated_text": result.text}
