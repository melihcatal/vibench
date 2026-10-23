import os
import deepl
from document_models import OCRTextResponse


DEEPL_AUTH_KEY = os.environ.get("DEEPL_AUTH_KEY", "")
DEEPL_TARGET_LANG = os.environ.get("DEEPL_TARGET_LANG", "EN")


def translate_ocr_text(ocr_response: OCRTextResponse, target_lang: str = None) -> dict:
    if not ocr_response or not ocr_response.text:
        return {
            "translated_text": "",
            "source_lang": "",
            "target_lang": target_lang or DEEPL_TARGET_LANG,
        }

    auth_key = DEEPL_AUTH_KEY
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")

    translator = deepl.Translator(auth_key)

    lang = target_lang or DEEPL_TARGET_LANG
    result = translator.translate_text(
        ocr_response.text,
        target_lang=lang,
    )

    return {
        "translated_text": result.text,
        "source_lang": result.detected_source_lang,
        "target_lang": result.target_lang,
        "original_text": ocr_response.text,
    }


def translate_text_string(text: str, target_lang: str = None) -> dict:
    if not text:
        return {
            "translated_text": "",
            "source_lang": "",
            "target_lang": target_lang or DEEPL_TARGET_LANG,
        }

    auth_key = DEEPL_AUTH_KEY
    if not auth_key:
        raise ValueError("DEEPL_AUTH_KEY environment variable is not set")

    translator = deepl.Translator(auth_key)

    lang = target_lang or DEEPL_TARGET_LANG
    result = translator.translate_text(
        text,
        target_lang=lang,
    )

    return {
        "translated_text": result.text,
        "source_lang": result.detected_source_lang,
        "target_lang": result.target_lang,
        "original_text": text,
    }
