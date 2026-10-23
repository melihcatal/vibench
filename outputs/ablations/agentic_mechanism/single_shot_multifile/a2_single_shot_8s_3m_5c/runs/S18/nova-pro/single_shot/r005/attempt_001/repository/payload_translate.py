from google.cloud import translate_v3

client = translate_v3.TranslationServiceClient()

parent = f'projects/your-project-id/locations/global'
texts = ['Text to translate']
response = client.translate_text(parent=parent, contents=texts, mime_type='text/plain', target_language_code='es')
for translation in response.translations:
    print(translation.translated_text)