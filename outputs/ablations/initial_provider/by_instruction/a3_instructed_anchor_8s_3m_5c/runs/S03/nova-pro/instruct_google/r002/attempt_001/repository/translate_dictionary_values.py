import os
from google.cloud import translate_v3 as translate

def translate_dictionary_values(dictionary, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('YOUR_PROJECT_ID', 'global')
    texts = list(dictionary.values())
    responses = client.translate_text(parent, texts, target_language)
    translated_dict = {key: response.translated_text for key, response in zip(dictionary.keys(), responses.translations)}
    return translated_dict