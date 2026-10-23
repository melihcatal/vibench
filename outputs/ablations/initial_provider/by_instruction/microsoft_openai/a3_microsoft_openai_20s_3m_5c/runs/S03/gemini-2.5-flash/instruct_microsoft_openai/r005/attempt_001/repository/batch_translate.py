import os
from google.cloud import translate

def batch_translate(texts: list[str], source_language: str, target_language: str, project_id: str) -> list[str]:
    """
    Translates a list of strings while preserving order using Google Cloud Translation API.

    Args:
        texts: A list of text strings to translate.
        source_language: The language of the input texts (e.g., "en", "fr").
        target_language: The language to translate the texts into (e.g., "es", "de").
        project_id: The Google Cloud project ID.

    Returns:
        A list of translated text strings, preserving the original order.
    """
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language,
            "source_language_code": source_language,
        }
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts
