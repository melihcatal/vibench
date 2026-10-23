from translation_client import get_translation_client, get_project_id
from translation_models import TranslationRequest, TranslationResponse


def translate_text(request: TranslationRequest) -> TranslationResponse:
    client = get_translation_client()
    project_id = get_project_id()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": request.texts,
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
            "mime_type": "text/plain",  # Use text/plain for plain text
        }
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return TranslationResponse(
        translated_texts=translated_texts, original_texts=request.texts
    )
