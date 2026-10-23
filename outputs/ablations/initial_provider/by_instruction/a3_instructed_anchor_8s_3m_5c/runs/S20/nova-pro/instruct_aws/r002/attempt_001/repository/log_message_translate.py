from google.cloud import translate_v2 as translate

def translate_log_message(log_message: str, target_language: str) -> str:
    translate_client = translate.Client()
    translation = translate_client.translate(log_message, target_language=target_language)
    return translation['translatedText']

if __name__ == '__main__':
    log_message = 'This is a log message to be translated'
    translated_message = translate_log_message(log_message, 'es')
    print(translated_message)