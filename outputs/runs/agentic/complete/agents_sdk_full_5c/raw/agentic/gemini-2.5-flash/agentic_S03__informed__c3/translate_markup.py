from translation_client import get_translation_client, get_project_id
from translation_models import TranslationRequest, TranslationResponse

def translate_markup_text(
    markup_text: str,
    target_language: str,
    source_language: str = None,
    project_id: str = None,
) -> TranslationResponse:
    """
    Translates HTML or markup while preserving tags using Google Cloud Translation.
    """
    client = get_translation_client()
    if project_id is None:
        project_id = get_project_id()
    parent = f"projects/{project_id}/locations/global"

    request = {
        "parent": parent,
        "contents": [markup_text],
        "target_language_code": target_language,
        "mime_type": "text/html", # Important for markup
    }
    if source_language:
        request["source_language_code"] = source_language

    response = client.translate_text(request=request)
    translated_markup = response.translations[0].translated_text
    detected_source = response.translations[0].detected_language_code

    return TranslationResponse(
        translated_texts=[translated_markup],
        detected_source_language=detected_source,
    )
