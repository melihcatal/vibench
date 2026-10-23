import os

GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

from google.cloud import translate_v3


def translate_text(text, target_language="en"):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{GOOGLE_APPLICATION_CREDENTIALS}/locations/global"
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language,
        }
    )
    return response.translations[0].translated_text
