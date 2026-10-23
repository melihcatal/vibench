import os
from google.cloud import translate_v3 as translate

def batch_translate(texts, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('YOUR_PROJECT_ID', 'global')
    responses = client.translate_text(parent, texts, target_language)
    return [response.translated_text for response in responses.translations]