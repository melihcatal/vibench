import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

client = TextTranslationClient(credential=TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY')), endpoint=os.getenv('AZURE_TRANSLATOR_REGION'))

def translate_alt_text(alt_text, target_language='es'):
    result = client.translate(content=[alt_text], to=[target_language])
    return result[0].translations[0].text