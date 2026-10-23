import os
from google.cloud import translate_v3 as translate

def translate_text(project_id: str, text: str, target_language_code: str, source_language_code: str = None) -> str:
    """Translates text using Google Cloud Translation API."""
    client = translate.TranslationServiceClient()
    parent = f"projects/{project_id}"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "target_language_code": target_language_code,
            "source_language_code": source_language_code,
        }
    )

    # The response can contain multiple translations, but we only sent one piece of content.
    for translation in response.translations:
        return translation.translated_text

    return ""

if __name__ == '__main__':
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    TEXT_TO_TRANSLATE = "Hello, world!"
    TARGET_LANG = "es"

    # Make sure to set GOOGLE_APPLICATION_CREDENTIALS environment variable
    # or authenticate otherwise.
    # translated_text = translate_text(PROJECT_ID, TEXT_TO_TRANSLATE, TARGET_LANG)
    # print(f"Original: {TEXT_TO_TRANSLATE}, Translated ({TARGET_LANG}): {translated_text}")
