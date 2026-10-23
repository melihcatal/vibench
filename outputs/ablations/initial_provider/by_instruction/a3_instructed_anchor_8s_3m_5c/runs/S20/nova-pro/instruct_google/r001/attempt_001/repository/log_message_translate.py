from google.cloud import translate

client = translate.TranslationServiceClient()

def translate_log_message(message, target_language_code):
    parent = client.location_path('your-project-id', 'us-central1')
    response = client.translate_text(parent, message, target_language_code)
    return response.translations[0].translated_text

log_message = 'This is a log message to be translated'
target_language_code = 'es'

translated_message = translate_log_message(log_message, target_language_code)
print(translated_message)