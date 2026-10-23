from google.cloud import translate_v3 as translate
from typing import List

def batch_translate_text(
    project_id: str,
    texts: List[str],
    source_language_code: str,
    target_language_code: str,
) -> List[str]:
    """Translates a list of strings while preserving order using Google Cloud Translation."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        source_language_code=source_language_code,
        target_language_code=target_language_code,
    )

    return [translation.translated_text for translation in response.translations]
