from google.cloud import translate_v3

def translate_text(text, target_language='en'):
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent=parent, contents=[text], mime_type='text/plain', target_language_code=target_language)
    for translation in response.translations:
        return translation.translated_text

# Example usage:
# translated_text = translate_text('Hola, ¿cómo estás?')
# print(translated_text)