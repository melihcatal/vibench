import os
from google.cloud import translate

def translate_script(text, target_language):
    client = translate.TranslationServiceClient()
    parent = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/global'
    response = client.translate_text(parent=parent, contents=[text], target_language_code=target_language)
    return response.translations[0].translated_text