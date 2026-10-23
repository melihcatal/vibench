import os
from google.cloud import translate

client = translate.TranslationServiceClient()

def translate_note(note, target_language_code):
    parent = client.location_path(os.getenv('GCP_PROJECT_ID'), 'global')
    response = client.translate_text(parent, [note], target_language_code)
    return response.translations[0].translated_text