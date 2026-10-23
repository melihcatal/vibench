from google.cloud import translate_v3 as translate
from translation_client import get_translation_client

def batch_translate(
    texts: list[str],
    target_language_code: str,
    source_language_code: str = None
) -> list[str]:
    """Translates a list of strings while preserving order using Google Cloud Translation."""
    client = get_translation_client()
    parent = f"projects/{client.project}"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",
    )
    return [translation.translated_text for translation in response.translations]
