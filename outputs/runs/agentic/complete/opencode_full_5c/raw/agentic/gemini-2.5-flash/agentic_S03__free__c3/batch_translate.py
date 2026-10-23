from translation_client import get_translation_client
from translation_models import get_project_id, get_location
from typing import List


def batch_translate_texts(
    texts: List[str], target_language: str, source_language: str = ""
) -> List[str]:
    """Translates a list of text strings using Google Cloud Translation V3, preserving order.

    Args:
        texts: A list of text strings to translate.
        target_language: The language to translate the texts to (e.g., "es" for Spanish).
        source_language: The language of the texts. If not specified, auto-detected.

    Returns:
        A list of translated texts in the same order as the input.
    """
    client = get_translation_client()
    project_id = get_project_id()
    location = get_location()

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return translated_texts
