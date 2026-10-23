import os
from typing import List

from google.cloud import translate_v3 as translate

def translate_queries(queries: List[str], target_language: str = "en") -> List[str]:
    client = translate.TranslationServiceClient()
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    location = os.environ.get("GOOGLE_CLOUD_LOCATION", "global")

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
    return translated_texts