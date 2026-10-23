import os
from google.cloud import translate_v3 as translate

def translate_markup(markup, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('YOUR_PROJECT_ID', 'global')
    response = client.translate_text(parent, markup, target_language)
    return response.translations[0].translated_text