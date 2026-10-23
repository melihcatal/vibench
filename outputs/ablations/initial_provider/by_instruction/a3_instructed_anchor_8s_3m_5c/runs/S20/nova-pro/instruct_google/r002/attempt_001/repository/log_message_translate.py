from google.cloud import translate

def translate_log_message(log_message, target_language):
    client = translate.TranslationServiceClient()
    parent = client.location_path('your-project-id', 'global')
    response = client.translate_text(parent, log_message, target_language)
    return response.translations[0].translated_text

if __name__ == '__main__':
    log_message = 'This is a log message'
    target_language = 'es'
    print(translate_log_message(log_message, target_language))