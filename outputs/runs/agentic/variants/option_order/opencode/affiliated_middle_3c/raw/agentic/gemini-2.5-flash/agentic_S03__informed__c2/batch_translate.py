import os
from typing import List
from translation_client import get_translation_client
from translation_models import TranslationRequest, TranslationResponse


def batch_translate_texts(
    requests: List[TranslationRequest],
) -> List[TranslationResponse]:
    """
    Translates a list of text strings while preserving order using Google Cloud Translation.
    """
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    contents = [req.text for req in requests]
    target_language_code = requests[0].target_language if requests else None
    source_language_code = requests[0].source_language if requests else None

    if not contents or not target_language_code:
        return []

    response = client.translate_text(
        parent=parent,
        contents=contents,
        target_language_code=target_language_code,
        source_language_code=source_language_code,
    )

    translated_responses = []
    for i, translation in enumerate(response.translations):
        translated_responses.append(
            TranslationResponse(
                translated_text=translation.translated_text,
                source_text=requests[i].text,
            )
        )
    return translated_responses
