import os
from typing import List, Dict, Any
from google.cloud import translate_v3 as translate  # Google Cloud Translation API


def translate_queries(
    queries: List[str], target_language: str = "en"
) -> Dict[str, List[str]]:
    """Translates queries before multilingual embedding search using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get(
        "GOOGLE_CLOUD_REGION", "global"
    )  # Translation API often uses 'global'

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/{location}"
    translated_texts = []

    for query in queries:
        response = client.translate_text(
            request={
                "parent": parent,
                "contents": [query],
                "target_language_code": target_language,
            }
        )
        for translation in response.translations:
            translated_texts.append(translation.translated_text)

    return {"translated_queries": translated_texts}
