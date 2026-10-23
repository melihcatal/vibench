from translation_client import get_translation_client
from typing import List


def batch_translate(
    texts: List[str], target_language_code: str, source_language_code: str = "en"
) -> List[str]:
    """Translates a list of strings while preserving order using Google Cloud Translation."""
    client = get_translation_client()
    project_id = ""  # Replace with your Google Cloud Project ID
    location = "global"

    parent = f"projects/{project_id}/locations/{location}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)
    return translated_texts
