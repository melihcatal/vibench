import os
from typing import List
from translation_client import get_translation_client

def batch_translate_texts(
    texts: List[str], target_language: str, source_language: str = ""
) -> List[str]:
    """Translates a list of texts using Google Cloud Translation API, preserving order.

    Args:
        texts: A list of text strings to translate.
        target_language: The language to translate the texts to (e.g., 'es' for Spanish).
        source_language: The language of the input texts (e.g., 'en' for English).
                         If not specified, Google will auto-detect.

    Returns:
        A list of translated texts in the same order as the input.
    """
    client = get_translation_client()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")

    if not project_id:
        raise ValueError(
            "GOOGLE_CLOUD_PROJECT_ID environment variable not set. "
            "Please set it to your Google Cloud Project ID."
        )

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language,
            "source_language_code": source_language if source_language else None,
        }
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return translated_texts
