import os
from typing import List, Dict, Any

from embeddings_client import get_translation_client


def multilingual_query_translate(
    query: str, target_languages: List[str]
) -> Dict[str, str]:
    """Translates queries before multilingual embedding search using Google Cloud Translation API.

    Args:
        query: The original query string.
        target_languages: A list of target language codes (e.g., ['es', 'fr']).

    Returns:
        A dictionary where keys are target language codes and values are the translated queries.
    """
    client = get_translation_client()
    project_id = os.environ.get("GCP_PROJECT_ID")
    location = os.environ.get(
        "GCP_LOCATION", "global"
    )  # Translation API often uses 'global' for location

    parent = f"projects/{project_id}/locations/{location}"
    translated_queries = {}

    for lang_code in target_languages:
        response = client.translate_text(
            parent=parent,
            contents=[query],
            target_language_code=lang_code,
        )
        for translation in response.translations:
            translated_queries[lang_code] = translation.translated_text

    return translated_queries
