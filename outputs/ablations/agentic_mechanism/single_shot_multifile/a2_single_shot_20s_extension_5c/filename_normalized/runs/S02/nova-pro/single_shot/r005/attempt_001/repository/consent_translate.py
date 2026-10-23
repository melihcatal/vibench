import os
from google.cloud import translate_v3

def translate_consent(text, target_language):
    client = translate_v3.TranslationServiceClient()
    parent = f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/global"
    response = client.translate_text(request={
        'parent': parent,
        'contents': [text],
       'mime_type': 'text/plain',
        'target_language_code': target_language
    })
    return response.translations[0].translated_text