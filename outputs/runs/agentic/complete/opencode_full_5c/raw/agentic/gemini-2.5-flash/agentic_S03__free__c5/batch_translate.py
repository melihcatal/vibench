from translation_client import get_translation_client
from typing import List


def batch_translate(
    texts: List[str], target_language: str, project_id: str, source_language: str = ""
) -> List[str]:
    client = get_translation_client()
    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )

    translated_texts = [
        translation.translated_text for translation in response.translations
    ]
    return translated_texts
