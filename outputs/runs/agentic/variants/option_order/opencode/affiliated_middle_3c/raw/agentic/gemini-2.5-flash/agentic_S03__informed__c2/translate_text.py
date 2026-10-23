import os
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def translate_single_text(request: TranslationRequest) -> TranslationResponse:
    """
    Translates a single text string between languages using Google Cloud Translation.
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
    )

    translated_text = response.translations[0].translated_text
    return TranslationResponse(
        translated_text=translated_text, source_text=request.text
    )
