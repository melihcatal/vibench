import os
from google.cloud import translate_v3

def translate_text(text, target_language='en'):
    """Translates text into the target language."""
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':
    description = 'Generated image description'
    translated_description = translate_text(description)
    print(f'Translated description: {translated_description}')
