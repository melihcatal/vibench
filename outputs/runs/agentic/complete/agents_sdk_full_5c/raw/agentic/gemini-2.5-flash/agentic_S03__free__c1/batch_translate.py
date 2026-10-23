from google.cloud import translate_v3
from translation_client import get_translation_client
from typing import List

def batch_translate_text(texts: List[str], target_language: str, source_language: str = None) -> List[str]:
    """Translates a list of strings using Google Cloud Translation, preserving order."""
    client = get_translation_client()
    parent = f"projects/{client.project}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": texts,
            "target_language_code": target_language,
            "source_language_code": source_language,
            "mime_type": "text/plain",
        }
    )

    return [translation.translated_text for translation in response.translations]

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # translated_texts = batch_translate_text(["Hello", "World"], "es", "en")
    # print(f"Translated texts: {translated_texts}")
    pass
