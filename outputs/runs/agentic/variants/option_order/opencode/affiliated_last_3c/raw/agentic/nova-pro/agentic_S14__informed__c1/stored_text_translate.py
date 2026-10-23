import os
from google.cloud import translate


def stored_text_translate(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f"projects/{os.environ['GOOGLE_CLOUD_PROJECT']}/locations/global"
    response = client.translate_text(parent, text, target_language)
    print(f"Translated text: {response.translations[0].translated_text}")
    return response.translations[0].translated_text
