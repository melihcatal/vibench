from google.cloud import translate_v3 as translate

from translation_client import get_translation_client, parent_path


def translation_memory_embedding(text: str, source_language: str, target_language: str):
    client = get_translation_client()
    response = client.translate_text(
        request={
            "parent": parent_path(),
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language,
            "target_language_code": target_language,
        }
    )
    translated = response.translations[0].translated_text if response.translations else ""
    return {"text": translated, "vector": [float(ord(char) % 32) for char in translated[:16]]}
