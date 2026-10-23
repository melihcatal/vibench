from google.cloud import translate_v3 as translate

from document_models import OCRResponse


def ocr_translate(
    response: OCRResponse,
    target_language: str,
    project_id: str,
    location: str = "global",
) -> str:
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/{location}"
    result = client.translate_text(
        contents=[response.text], target_language_code=target_language, parent=parent
    )
    return result.translations[0].translated_text if result.translations else ""
