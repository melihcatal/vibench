import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

client = TextTranslationClient(credential=TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY')), endpoint=os.getenv('AZURE_TRANSLATOR_REGION'))

def summarize_image(description):
    result = client.translate(content=[description], to=['en'])
    return result[0].translations[0].text