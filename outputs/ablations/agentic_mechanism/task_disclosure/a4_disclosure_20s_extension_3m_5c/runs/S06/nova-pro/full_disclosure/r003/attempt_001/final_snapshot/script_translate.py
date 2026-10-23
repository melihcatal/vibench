from google.cloud import translate_v3

def translate_text(text, target_language):
    client = translate_v3.TranslationServiceClient()
    parent = client.location_path('YOUR_PROJECT_ID', 'global')
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':
    text = 'Hello, world!'
    target_language = 'es'
    translated_text = translate_text(text, target_language)
    print(f'Translated text: {translated_text}')
