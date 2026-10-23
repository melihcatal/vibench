import os
from translate import Translator
from document_client import DocumentClient
from document_models import TranslationRequest, TranslationResponse

def translate_text(source_lang: str, target_lang: str, text: str) -> str:
    """Translate OCR-extracted text using the googletrans library.",
    # googletrans is a free, lightweight wrapper around Google Translate API.
    translator = Translator()
    translation = translator.translate(text, src=source_lang, dest=target_lang)
    return translation.text


def translate_document_text(image_path: str, source_lang: str = "en", target_lang: str = "es") -> str:
    """Extract text via OCR and translate the result in a single step.",
    client = DocumentClient(service="azure_ocr")  # any OCR client works here
    with open(image_path, "rb") as img:
        ocr_text = client.ocr_image(image_bytes=img.read())
        extracted_text = ocr_text.get("text", "")
    translated = translate_text(source_lang, target_lang, extracted_text)
    return translated
