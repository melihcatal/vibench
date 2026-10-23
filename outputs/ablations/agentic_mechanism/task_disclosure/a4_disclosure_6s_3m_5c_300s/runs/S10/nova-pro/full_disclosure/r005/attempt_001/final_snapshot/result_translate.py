from google.cloud import translate

def translate_text(text, target_language='en'):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, text, target_language)
    translated_text = response.translations[0].translated_text
    return translated_text