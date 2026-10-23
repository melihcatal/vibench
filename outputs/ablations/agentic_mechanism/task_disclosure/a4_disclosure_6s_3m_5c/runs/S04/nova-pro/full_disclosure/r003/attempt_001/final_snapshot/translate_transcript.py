from google.cloud import translate_v3

def translate_text(text, target_language):
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(request={
        'parent': parent,
        'contents': [text],
        'mime_type': 'text/plain',
        'target_language_code': target_language
    })
    return response.translations[0].translated_text

# Example usage
# translated_text = translate_text('Hello, world!', 'es')