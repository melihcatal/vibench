from translation_client import get_translation_client, get_project_id
from translation_models import MarkupTranslationRequest, MarkupTranslationResponse


def translate_markup(request: MarkupTranslationRequest) -> MarkupTranslationResponse:
    client = get_translation_client()
    project_id = get_project_id()

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [request.markup_text],
            "target_language_code": request.target_language_code,
            "source_language_code": request.source_language_code,
            "mime_type": "text/html",  # Use text/html for markup
        }
    )

    translated_markup = response.translations[0].translated_text
    return MarkupTranslationResponse(translated_markup=translated_markup)
