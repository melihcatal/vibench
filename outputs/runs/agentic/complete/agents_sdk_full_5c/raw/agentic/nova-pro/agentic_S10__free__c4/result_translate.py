from google.cloud import translate

def translate_text(text, target_language='en'):
    client = translate.TranslationServiceClient()
    location = 'global'
    parent = f'projects/my-project-id/locations/{location}'
    response = client.translate_text(parent=parent, contents=[text], mime_type='text/plain', target_language_code=target_language)
    return response.translations[0].translated_text