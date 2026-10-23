import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationApiKeyCredential

def translate_log_message(log_message, to_language='es'):
    endpoint = os.environ['TRANSLATION_ENDPOINT']
    key = os.environ['TRANSLATION_KEY']
    client = TextTranslationClient(endpoint=endpoint, credential=TextTranslationApiKeyCredential(key))
    result = client.translate([log_message], to_language)
    return result[0].translations[0].text

log_message = 'This is a sample log message.'
print(translate_log_message(log_message))