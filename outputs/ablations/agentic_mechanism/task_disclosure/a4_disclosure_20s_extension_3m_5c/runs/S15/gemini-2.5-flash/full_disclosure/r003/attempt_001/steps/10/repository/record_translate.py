
import os
from google.cloud import translate_v3 as translate

def translate_text(text: str, target_language: str, project_id: str) -> str:
    """Translates a given text to the target language using Google Cloud Translation."""

    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language,
    )

    return response.translations[0].translated_text

if __name__ == '__main__':
    # Example usage (replace with your actual project ID and text)
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    text_to_translate = "Hello, world!"
    target_lang = "es"  # Spanish

    translated_content = translate_text(text_to_translate, target_lang, project_id)
    print(f"Original text: {text_to_translate}")
    print(f"Translated text ({target_lang}): {translated_content}")
