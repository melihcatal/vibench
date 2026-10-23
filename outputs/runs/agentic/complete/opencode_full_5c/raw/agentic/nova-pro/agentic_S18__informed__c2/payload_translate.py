import os
from google.cloud import translate_v3

client = translate_v3.TranslationServiceClient()


def payload_translate(text, target_language_code):
    parent = client.location_path(os.getenv("GOOGLE_CLOUD_PROJECT"), "global")
    response = client.translate_text(
        request={
            "parent": parent,
            "contents": [text],
            "mime_type": "text/plain",
            "target_language_code": target_language_code,
        }
    )
    return response.translations[0].translated_text
