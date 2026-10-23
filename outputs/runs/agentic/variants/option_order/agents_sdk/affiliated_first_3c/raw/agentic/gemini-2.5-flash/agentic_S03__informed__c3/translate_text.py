from google.cloud import translate_v3 as translate
from translation_client import get_translation_client

def translate_text(
    text: str,
    target_language_code: str,
    source_language_code: str = None
) -> str:
    """Translates a single text string using Google Cloud Translation."""
    client = get_translation_client()
    parent = f"projects/{client.project}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",
    )
    return response.translations[0].translated_text
