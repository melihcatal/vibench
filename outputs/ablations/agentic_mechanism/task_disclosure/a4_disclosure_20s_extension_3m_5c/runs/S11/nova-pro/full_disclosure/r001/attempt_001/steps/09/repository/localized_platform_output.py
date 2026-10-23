import os

from google.cloud import translate_v3 as translate

def translate_text(text, target_language):
    """Translates text into the target language."""
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent=parent, contents=[text], mime_type='text/plain', target_language_code=target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':
    original_text = 'Hello, world!'
    translated_text = translate_text(original_text, 'es')
    print(translated_text)