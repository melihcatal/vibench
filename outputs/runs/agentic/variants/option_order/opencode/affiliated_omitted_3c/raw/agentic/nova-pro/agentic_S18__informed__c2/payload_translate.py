import os
from google.cloud import translate_v3


def payload_translate(text, target_language):
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path("your-project-id", "global")
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text
