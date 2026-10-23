from google.cloud import translate_v2 as translate
from document_models import TranslationRequest, TranslationResponse

def translate_ocr_text(request: TranslationRequest) -> TranslationResponse:
    """Translates extracted OCR text using Google Cloud Translation API."""
    translate_client = translate.Client()

    result = translate_client.translate(
        request.text_content,
        target_language=request.target_language,
        source_language=request.source_language
    )

    translated_text = result['translatedText']
    detected_source_language = result['detectedSourceLanguage'] if 'detectedSourceLanguage' in result else None

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language
    )
