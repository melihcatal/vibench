from typing import List
from translation_client import get_translation_client, get_gcp_project_id

def batch_translate_texts(
    texts: List[str], target_language_code: str, source_language_code: str
) -> List[str]:
    """
    Translates a list of text strings to a target language using Google Cloud Translate.

    Args:
        texts: The list of strings to translate.
        target_language_code: The ISO 639-1 code of the target language.
        source_language_code: The ISO 639-1 code of the source language.

    Returns:
        A list of translated texts in the same order as the input.
    """
    client = get_translation_client()
    project_id = get_gcp_project_id()
    
    response = client.translate_text(
        parent=f"projects/{project_id}",
        contents=texts,
        mime_type="text/plain",
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )
    
    return [translation.translated_text for translation in response.translations]
