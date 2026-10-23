import os
from typing import List, Dict, Any
from google.cloud import translate_v3 as translate

def translate_queries_for_multilingual_embedding(queries: List[str], target_language_code: str = "en") -> List[Dict[str, str]]:
    """Translates queries to a target language using Google Cloud Translation API
    before multilingual embedding search.

    Args:
        queries: A list of query strings to translate.
        target_language_code: The BCP-47 language code of the target language.

    Returns:
        A list of dictionaries, each containing the original query and its translation.
    """
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    parent = f"projects/{project_id}/locations/global"

    translations = []
    for query in queries:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [query],
                "target_language_code": target_language_code,
            }
        )
        translated_text = response.translations[0].translated_text if response.translations else query
        translations.append({"original_query": query, "translated_query": translated_text})
    return translations

