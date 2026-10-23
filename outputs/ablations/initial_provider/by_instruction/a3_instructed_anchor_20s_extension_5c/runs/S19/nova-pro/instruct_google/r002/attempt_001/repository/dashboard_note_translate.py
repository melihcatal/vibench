from google.cloud import translate_v3

def dashboard_note_translate(text, target_language):
    client = translate_v3.TranslationServiceClient()
    parent = f'projects/-/locations/-/'
    response = client.translate_text(request={
        'parent': parent,
        'contents': [text],
        'target_language_code': target_language,
    }
    )
    return response.translations[0].translated_text