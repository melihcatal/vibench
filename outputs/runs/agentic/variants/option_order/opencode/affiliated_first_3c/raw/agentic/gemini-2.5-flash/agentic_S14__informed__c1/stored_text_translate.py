from google.cloud import translate_v3 as translate
from storage_models import StoredTextTranslateRequest, StoredTextTranslateResponse


def translate_stored_text(
    request: StoredTextTranslateRequest,
) -> StoredTextTranslateResponse:
    """Translates text extracted from a stored document using Google Cloud Translation."""
    client = translate.TranslationServiceClient()

    parent = f"projects/{request.project_id}/locations/{request.location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
            "mime_type": "text/plain",
        }
    )

    translated_text = response.translations[0].translated_text
    detected_language_code = response.translations[0].detected_language_code

    return StoredTextTranslateResponse(
        translated_text=translated_text, detected_language_code=detected_language_code
    )
