from google.cloud import translate_v2 as translate

def translate_log_message(log_message, target_language):
    client = translate.Client()
    result = client.translate(log_message, target_language=target_language)
    return result['translatedText']

log_message = 'User logged in'
print(translate_log_message(log_message, 'es'))