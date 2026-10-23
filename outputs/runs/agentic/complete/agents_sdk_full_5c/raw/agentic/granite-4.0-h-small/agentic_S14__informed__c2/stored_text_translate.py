import os
from storage_models import OCRResult, TranslationResult
from google.cloud import translate_v2 as translate

def translate_ocr_text(ocr_result: OCRResult, target_lang='fr'):
    """Translate text extracted from OCR using Google Cloud Translation.

    Returns a TranslationResult with translated text and language metadata.
    """
    client = translate.Client()
    result = client.translate(ocr_result.text, target_language=target_lang)
    translated = result['translatedText']
    source_lang = result.get('detectedSourceLanguage', 'unknown')
    return TranslationResult(
        translated_text=translated,
        source_language=source_lang,
        target_language=target_lang
    )
