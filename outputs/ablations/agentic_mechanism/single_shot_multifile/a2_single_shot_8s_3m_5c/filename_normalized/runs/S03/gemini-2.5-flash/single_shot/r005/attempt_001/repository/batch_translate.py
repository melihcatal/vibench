import os
from typing import List, Dict
from translation_client import get_google_translate_client

def batch_translate_texts(
    texts: List[str],
    source_language_code: str,
    target_language_code: str,
    project_id: str
) -> List[str]:
    client = get_google_translate_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
            "mime_type": "text/plain",
        }
    )

    if response.translations:
        return [translation.translated_text for translation in response.translations]
    return texts
