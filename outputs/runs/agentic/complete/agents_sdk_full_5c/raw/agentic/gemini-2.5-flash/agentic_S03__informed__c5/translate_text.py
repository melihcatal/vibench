import os
from translation_client import get_translation_client

def translate_single_text(text: str, target_language: str, source_language: str = "en") -> str:
    """Translates a single text string using Google Cloud Translation."""
    client = get_translation_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    parent = f"projects/{project_id}/locations/global"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        mime_type="text/plain",
        source_language_code=source_language,
        target_language_code=target_language,
    )

    translated_text = response.translations[0].translated_text
    return translated_text

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT env vars)
    # text_to_translate = "Hello, world!"
    # target_lang = "es"
    # translated = translate_single_text(text_to_translate, target_lang)
    # print(f"Original: {text_to_translate}")
    # print(f"Translated ({target_lang}): {translated}")
    pass
