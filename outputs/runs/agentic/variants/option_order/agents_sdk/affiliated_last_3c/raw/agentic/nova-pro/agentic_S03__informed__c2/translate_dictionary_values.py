import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput

client = TextTranslationClient(endpoint=os.getenv('AZURE_TRANSLATOR_ENDPOINT'), credential=os.getenv('AZURE_TRANSLATOR_KEY'))

def translate_dictionary_values(dictionary, to_language):
    texts = list(dictionary.values())
    input = TextTranslationInput(text=texts, to=[to_language] * len(texts))
    response = client.translate(input)
    translated_dict = dict(zip(dictionary.keys(), [t.translations[0].text for t in response]))
    return translated_dict