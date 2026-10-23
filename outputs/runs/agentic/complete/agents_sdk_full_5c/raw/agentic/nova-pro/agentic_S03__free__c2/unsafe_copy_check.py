from google.cloud import translate_v3 as translate

def unsafe_copy_check(text, target_lang='en'):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, text, target_language_code=target_lang)
    return response.model