from google.cloud import translate_v3 as translate
import os

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")

def translate_text(text: str, target_language_code: str = "es", source_language_code: str = "en") -> str:
    client = translate.TranslationServiceClient()

    parent = f"projects/{PROJECT_ID}/locations/global"

    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "source_language_code": source_language_code,
            "target_language_code": target_language_code,
        }
    )

    if response.translations:
        return response.translations[0].translated_text
    return ""
