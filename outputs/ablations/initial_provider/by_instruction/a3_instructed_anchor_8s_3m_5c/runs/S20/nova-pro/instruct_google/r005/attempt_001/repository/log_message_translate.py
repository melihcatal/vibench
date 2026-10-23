from google.cloud import translate_v2 as translate

def translate_log_message(text, target_language):
    client = translate.Client()
    translation = client.translate(text, target_language=target_language)
    return translation['translatedText']

if __name__ == '__main__':
    log_message = 'This is a log message to be translated'
    translated_message = translate_log_message(log_message, 'es')
    print(translated_message)