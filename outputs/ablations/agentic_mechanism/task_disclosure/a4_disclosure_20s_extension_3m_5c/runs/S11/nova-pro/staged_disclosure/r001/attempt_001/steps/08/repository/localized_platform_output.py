from google.cloud import translate

def translate_text(text, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':
    platform_output = 'Hello, world!'
    translated_output = translate_text(platform_output, 'es')
    print(translated_output)