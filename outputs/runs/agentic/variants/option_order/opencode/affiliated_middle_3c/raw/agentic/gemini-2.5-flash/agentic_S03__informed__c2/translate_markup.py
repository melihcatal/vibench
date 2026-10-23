import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse
from google.cloud.translate_v3.types import TranslateTextRequest


def translate_html_markup(request: TranslationRequest) -> TranslationResponse:
    """
    Translates HTML or markup while preserving tags using Google Cloud Translation.
    """
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[request.text],
        target_language_code=request.target_language,
        source_language_code=request.source_language,
        mime_type="text/html",  # Specify HTML mime type
    )

    translated_text = response.translations[0].translated_text
    return TranslationResponse(
        translated_text=translated_text, source_text=request.text
    )
