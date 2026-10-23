import os
from google.cloud import translate

client = translate.TranslationServiceClient()

text = 'This is a log message.'
response = client.translate_text(request={'parent': 'projects/YOUR_PROJECT_ID/locations/global', 'contents': [text], 'mime_type': 'text/plain', 'target_language_code': 'es'})

for translation in response.translations:
    print(translation.translated_text)