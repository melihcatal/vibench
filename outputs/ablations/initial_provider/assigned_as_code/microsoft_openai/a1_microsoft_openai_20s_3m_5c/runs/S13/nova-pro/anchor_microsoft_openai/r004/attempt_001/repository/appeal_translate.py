from google.cloud import translate_v3

def translate_appeal(text, target_language):
    client = translate_v3.TranslationServiceClient()
    location = 'global'
    parent = f'projects/YOUR_PROJECT_ID/locations/{location}'
    response = client.translate_text(request={'parent': parent, 'contents': [text], 'mime_type': 'text/plain', 'target_language_code': target_language})
    return response.translations[0].translated_text