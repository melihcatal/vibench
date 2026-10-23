import os
from google.cloud import translate
from document_models import OCRTranslationRequest, OCRTranslationResult


def translate_ocr_text(request: OCRTranslationRequest) -> OCRTranslationResult:
    client = translate.TranslationServiceClient()

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable must be set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request=translate.TranslateTextRequest(
            parent=parent,
            contents=[request.text],
            target_language_code=request.target_language,
        )
    )

    translated_text = ""
    source_language = None
    if response.translations:
        translated_text = response.translations[0].translated_text
        source_language = response.translations[0].detected_language_code

    return OCRTranslationResult(
        translated_text=translated_text, source_language=source_language
    )
