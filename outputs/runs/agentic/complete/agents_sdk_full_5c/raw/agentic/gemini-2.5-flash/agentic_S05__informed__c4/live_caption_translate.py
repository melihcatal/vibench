import os
from google.cloud import translate_v3 as translate

# Google Cloud Translation configuration
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

def translate_caption(text: str, target_language_code: str = "es", source_language_code: str = "en-US") -> str:
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = translate.TranslationServiceClient()
    parent = f"projects/{PROJECT_ID}"

    response = client.translate_text(
        parent=parent,
        contents=[text],
        target_language_code=target_language_code,
        source_language_code=source_language_code,
        mime_type="text/plain",
    )

    translated_text = ""
    for translation in response.translations:
        translated_text += translation.translated_text
    return translated_text
