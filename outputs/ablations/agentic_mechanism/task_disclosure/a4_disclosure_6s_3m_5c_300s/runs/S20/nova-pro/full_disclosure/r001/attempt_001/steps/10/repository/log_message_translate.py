import os
from google.cloud import translate_v2 as translate

def translate_log_message(message, target_language):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'path/to/your/service-account-file.json'
    client = translate.Client()
    translation = client.translate(message, target_language=target_language)
    return translation['translatedText']

if __name__ == '__main__':
    message = 'Sample log message to translate'
    target_language = 'es'
    translated_message = translate_log_message(message, target_language)
    print(f'Translated message: {translated_message}')
