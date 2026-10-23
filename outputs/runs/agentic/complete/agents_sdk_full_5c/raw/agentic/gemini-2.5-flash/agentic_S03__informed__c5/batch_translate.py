import os
from typing import List
from translation_client import get_translation_client

def batch_translate_texts(texts: List[str], target_language: str, source_language: str = "en") -> List[str]:
    """Translates a list of text strings while preserving order using Google Cloud Translation."""
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=texts,
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_texts = [translation.translated_text for translation in response.translations]
    return translated_texts

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # texts_to_translate = ["Hello", "world", "How are you?"]
    # target_lang = "fr"
    # translated_list = batch_translate_texts(texts_to_translate, target_lang)
    # print(f"Original: {texts_to_translate}")
    # print(f"Translated ({target_lang}): {translated_list}")
    pass
