GOOGLE_CLOUD_PROJECT')}/locations/global'
    response = client.translate_text(request={'parent': parent, 'contents': [text], 'target_language_code': target_language})
    return response.translations[0].translated_text