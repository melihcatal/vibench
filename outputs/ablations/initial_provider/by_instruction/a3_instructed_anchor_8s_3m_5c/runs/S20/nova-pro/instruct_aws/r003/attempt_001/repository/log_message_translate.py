from google.cloud import translate_v2 as translate

def translate_log_message(log_message, target_language):
    client = translate.Client()
    translation = client.translate(log_message, target_language=target_language)
    return translation['translatedText']

if __name__ == '__main__':
    print(translate_log_message('This is an example log message.', 'es'))
