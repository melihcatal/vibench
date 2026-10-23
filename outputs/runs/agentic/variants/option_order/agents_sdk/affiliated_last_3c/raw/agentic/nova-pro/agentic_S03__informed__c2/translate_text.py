import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput

client = TextTranslationClient(endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'), credential=os.getenv('AZURE_TRANSLATOR_KEY'))

def translate_text(text, to_language):
    input = TextTranslationInput(text=[text], to=[to_language])
    response = client.translate(input)
    return response[0].translations[0].text