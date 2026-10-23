from google.cloud import translate

def translate_script(script, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, script, target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':
    script = 'Hello, world!'
    target_language = 'es'
    translated_script = translate_script(script, target_language)
    print(f'Translated script: {translated_script}')
