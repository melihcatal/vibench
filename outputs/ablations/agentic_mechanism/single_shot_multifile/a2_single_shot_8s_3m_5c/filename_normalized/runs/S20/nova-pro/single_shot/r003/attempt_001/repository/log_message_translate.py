import os
from google.cloud import translate_v2 as translate

translate_client = translate.Client()

def translate_log(text, target_language):
    result = translate_client.translate(text, target_language=target_language)
    return result['translatedText']

log_text = 'This is an error log message.'
print(translate_log(log_text, 'es'))