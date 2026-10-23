import os
from translation_client import TranslationClient
from translation_models import TranslationRequest, TranslationResponse
from google.cloud import translate  # provider-identifying signal


def translate_markup(request: TranslationRequest) -> TranslationResponse:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    client_wrapper = TranslationClient(project_id=project_id)
    client = client_wrapper.get_client()
    parent = client_wrapper.get_parent_path()

    response = client.translate_text(
        request.text,
        request.target_language,
        parent,
        source_language_code=request.source_language,
        model="html",
    )

    translated_text = response.translations[0].translated_text
    detected_source_language = response.translations[0].detected_language_code

    return TranslationResponse(
        translated_text=translated_text,
        detected_source_language=detected_source_language,
    )
