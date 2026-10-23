import os
from google.cloud import translate_v2 as translate

client = translate.Client()

def translate_log(log_text, target_language):
    response = client.translate(log_text, target_language=target_language)
    return response['translatedText']