import os
from google.cloud import translate_v3 as translate
from document_models import OcrTranslateRequest, OcrTranslateResponse

def translate_ocr_text(request: OcrTranslateRequest) -> OcrTranslateResponse:
    """Translates extracted OCR text using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text_content],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code, # Optional
        }
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code

    return OcrTranslateResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language
    )
