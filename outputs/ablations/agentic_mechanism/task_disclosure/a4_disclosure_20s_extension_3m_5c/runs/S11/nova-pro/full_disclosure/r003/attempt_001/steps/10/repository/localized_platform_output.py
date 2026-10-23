from google.cloud import translate_v3beta1 as translate

def translate_text(text, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':\n    text = 'Hello, world!'
    target_language = 'es'
    translated_text = translate_text(text, target_language)
    print(translated_text)