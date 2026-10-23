from google.cloud import translate

def translate_text(text, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, text, target_language)
    return response.translations[0].translated_text

# Example usage
translated_text = translate_text('Hello, world!', 'es')
print(translated_text)