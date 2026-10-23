from google.cloud import translate

def translate_text(text, target_language='es'):
    client = translate.TranslationServiceClient()
    parent = f'projects/YOUR_PROJECT_ID/locations/global'
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text