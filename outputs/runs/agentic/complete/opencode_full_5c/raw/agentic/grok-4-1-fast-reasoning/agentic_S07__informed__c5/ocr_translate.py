import os
import deepl
from document_models import OCRText


def ocr_translate(
    ocr_text: OCRText, source_lang: str = "auto", target_lang: str = "EN-US"
) -> OCRText:
    auth_key = os.getenv("DEEPL_AUTH_KEY")
    if not auth_key:
        raise ValueError("Set DEEPL_AUTH_KEY")
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(
        ocr_text, source_lang=source_lang, target_lang=target_lang
    )
    return result.text
