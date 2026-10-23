import os
from google.cloud import translate_v3 as translate

def translate_dictionary_values(dictionary, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/credentials.json'
    client = translate.TranslationServiceClient()
    location = 'global'
    translated_dict = {}
    for key, value in dictionary.items():
        parent = client.location_path(project='your-project-id', location=location)
        response = client.translate_text(parent=parent, contents=[value], mime_type='text/plain', target_language_code=target_language)
        translated_dict[key] = response.translations[0].translated_text
    return translated_dict