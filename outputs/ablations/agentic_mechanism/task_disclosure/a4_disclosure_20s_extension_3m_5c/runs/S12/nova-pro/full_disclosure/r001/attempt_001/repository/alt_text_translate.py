from google.cloud import translate

def translate_text(text, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, text, target_language, model='projects/your-project-id/locations/global/models/general-nmt')
    translated_texts = []
    for translation in response.translations:
        translated_texts.append(translation.translated_text)
    return translated_texts[0] if translated_texts else None