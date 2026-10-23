from typing import List
from translation_client import get_translation_client, get_gcp_project_id

def batch_translate_text(
    texts: List[str], target_language: str, source_language: str
) -> List[str]:
    """
    Translates a list of strings in a single batch request.

    Args:
        texts: A list of strings to translate.
        target_language: The ISO 639-1 code of the target language.
        source_language: The ISO 639-1 code of the source language.

    Returns:
        A list of translated strings, in the same order as the input.
    """
    if not texts:
        return []

    client = get_translation_client()
    project_id = get_gcp_project_id()

    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language,
        source_language_code=source_language,
        mime_type="text/plain",
    )

    return [translation.translated_text for translation in response.translations]
