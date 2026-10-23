import os
import deepl
from document_models import OCRTextResult


def translate_ocr_text(
    text_results: list[OCRTextResult], target_lang: str
) -> list[dict]:
    auth_key = os.environ["DEEPL_AUTH_KEY"]
    translator = deepl.Translator(auth_key)
    translated = []
    for result in text_results:
        if result.text:
            translation = translator.translate_text(
                result.text, target_lang=target_lang
            )
            translated.append(
                {
                    "page_number": result.page_number,
                    "original_text": result.text,
                    "translated_text": translation.text,
                    "target_lang": target_lang,
                }
            )
    return translated
