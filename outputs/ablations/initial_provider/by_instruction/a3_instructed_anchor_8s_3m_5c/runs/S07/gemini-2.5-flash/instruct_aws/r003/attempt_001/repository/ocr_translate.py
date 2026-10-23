from document_client import get_translate_client
from document_models import OcrTranslateRequest, OcrTranslateResponse

def translate_ocr_text(request: OcrTranslateRequest) -> OcrTranslateResponse:
    translate_client = get_translate_client()
    response = translate_client.translate_text(
        Text=request.text,
        SourceLanguageCode=request.source_language_code,
        TargetLanguageCode=request.target_language_code
    )
    return OcrTranslateResponse(
        translated_text=response['TranslatedText'],
        source_language_code=response['SourceLanguageCode'],
        target_language_code=response['TargetLanguageCode']
    )
