import os
from google.cloud import translate_v3

def translate_markup(content, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/credentials.json'
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, contents=[content], mime_type='text/html', target_language_code=target_language)
    return response.translations[0].translated_text