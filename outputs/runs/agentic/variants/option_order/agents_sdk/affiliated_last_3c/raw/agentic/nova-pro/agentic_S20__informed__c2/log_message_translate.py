import os
from google.cloud import translate

client = translate.TranslationServiceClient()

text = 'This is a log message'
parent = f'projects/{os.getenv("GOOGLE_CLOUD_PROJECT")}/locations/global'
response = client.translate_text(parent, text, 'es')
print(response.translations[0].translated_text)