from google.cloud import translate_v3 as translate
from translation_client import get_translation_client

def translate_dictionary_values(
    data: dict,
    target_language_code: str,
    source_language_code: str = None
) -> dict:
    """Translates dictionary values while preserving keys using Google Cloud Translation."""
    client = get_translation_client()
    parent = f"projects/{client.project}"

    texts_to_translate = list(data.values())
    original_keys = list(data.keys())

    response = client.translate_text(
        parent=parent,
        contents=texts_to_translate,
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    translated_data = {original_keys[i]: translated_texts[i] for i in range(len(original_keys))}
    return translated_data
