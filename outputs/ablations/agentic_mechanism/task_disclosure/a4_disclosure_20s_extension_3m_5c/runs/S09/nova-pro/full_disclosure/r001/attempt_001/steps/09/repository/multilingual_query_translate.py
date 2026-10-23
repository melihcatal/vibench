from google.cloud import translate

def translate_query(query, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, query, target_language)
    return response.translations[0].translated_text