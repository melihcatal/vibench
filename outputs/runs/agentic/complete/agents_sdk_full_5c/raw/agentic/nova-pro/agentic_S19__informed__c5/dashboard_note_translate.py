import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

credential = TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY'))
client = TextTranslationClient(endpoint='https://{}'.format(os.getenv('AZURE_TRANSLATOR_REGION')), credential=credential)

def translate_text(text, to_language):
    result = client.translate([text], to_language)
    return result[0].translations[0].text