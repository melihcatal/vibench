import os
from google.cloud import translate_v2 as translate

def translate_message(message, target_language):
    client = translate.Client()
    result = client.translate(message, target_language=target_language)
    return result['translatedText']

message = 'This is an example log message.'
translated_message = translate_message(message, 'es')
print(translated_message)