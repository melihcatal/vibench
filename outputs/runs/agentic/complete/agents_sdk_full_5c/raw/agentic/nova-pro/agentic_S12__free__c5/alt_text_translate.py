from google.cloud import translate

def translate_text(text, target_language='es'):
    client = translate.TranslationServiceClient()
    parent = f'projects/YOUR_PROJECT_ID/locations/global'
    response = client.translate_text(parent, text, target_language_code=target_language)
    translated_text = response.translations[0].translated_text
    print('Translated Text:', translated_text)