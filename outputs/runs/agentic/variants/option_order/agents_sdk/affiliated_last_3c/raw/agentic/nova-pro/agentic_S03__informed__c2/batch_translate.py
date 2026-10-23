import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput

client = TextTranslationClient(endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'), credential=os.getenv('AZURE_TRANSLATOR_KEY'))

def batch_translate(texts, to_language):
    input = TextTranslationInput(text=texts, to=[to_language] * len(texts))
    response = client.translate(input)
    return [t.translations[0].text for t in response]