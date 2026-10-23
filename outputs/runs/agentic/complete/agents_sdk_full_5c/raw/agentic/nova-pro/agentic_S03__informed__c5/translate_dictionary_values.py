import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationInput

client = TextTranslationClient(endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com", credential=os.getenv('AZURE_TRANSLATOR_KEY'))

def translate_dictionary_values(dictionary, to_language):
    input_texts = [TextTranslationInput(text=value, to=[to_language]) for value in dictionary.values()]
    results = client.translate_batch(input_texts)
    translated_values = [result.translations[0].text for result in results]
    return dict(zip(dictionary.keys(), translated_values))
