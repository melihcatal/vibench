from google.cloud import translate

def translate_runbook_notes(notes, target_language):
    client = translate.TranslationServiceClient()
    location = 'global'
    parent = client.location_path('your-project-id', location)
    response = client.translate_text(parent, notes, target_language)
    return [translation.translated_text for translation in response.translations]