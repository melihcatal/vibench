from translation_client import get_translation_client, get_project_id
from translation_models import TranslationRequest, TranslationResponse
from typing import List

def batch_translate_texts(
    texts: List[str],
    target_language: str,
    source_language: str = None,
    project_id: str = None,
) -> TranslationResponse:
    """
    Translates a list of text strings using Google Cloud Translation, preserving order.
    """
    client = get_translation_client()
    if project_id is None:
        project_id = get_project_id()
    parent = f"projects/{project_id}/locations/global"

    request = {
        "parent": parent,
        "contents": texts,
        "target_language_code": target_language,
        "mime_type": "text/plain",
    }
    if source_language:
        request["source_language_code"] = source_language

    response = client.translate_text(request=request)
    translated_texts = [translation.translated_text for translation in response.translations]
    detected_source = (
        response.translations[0].detected_language_code
        if response.translations
        else None
    )

    return TranslationResponse(
        translated_texts=translated_texts,
        detected_source_language=detected_source,
    )
