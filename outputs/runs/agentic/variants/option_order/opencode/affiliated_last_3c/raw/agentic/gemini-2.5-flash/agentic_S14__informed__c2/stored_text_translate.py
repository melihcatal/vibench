import os
from typing import List
from storage_client import StorageClient


def translate_text(
    project_id: str,
    location: str,
    texts: List[str],
    target_language_code: str,
    source_language_code: str = "en",
) -> List[str]:
    """Translates a list of texts using Google Cloud Translation AI.

    Args:
        project_id (str): Your Google Cloud project ID.
        location (str): The location of the translation service (e.g., "global").
        texts (List[str]): The list of texts to translate.
        target_language_code (str): The BCP-47 language code of the target language (e.g., "es" for Spanish).
        source_language_code (str): The BCP-47 language code of the source language (e.g., "en" for English).

    Returns:
        List[str]: A list of translated texts.
    """
    translate_client = StorageClient.get_translate_client()

    parent = f"projects/{project_id}/locations/{location}"

    responses = translate_client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    translated_texts = []
    for response in responses.translations:
        translated_texts.append(response.translated_text)

    print(f"Translated {len(texts)} texts to {target_language_code}.")
    return translated_texts
