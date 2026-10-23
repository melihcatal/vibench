import os
from google.cloud import translate

client = translate.TranslationServiceClient()

def translate_text(text, target_language='es'):
    parent = f'projects/YOUR_PROJECT_ID/locations/global'
    response = client.translate_text(parent=parent, contents=[text], target_language_code=target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':
    translated_text = translate_text('This is a description of an image.')
    print(translated_text)