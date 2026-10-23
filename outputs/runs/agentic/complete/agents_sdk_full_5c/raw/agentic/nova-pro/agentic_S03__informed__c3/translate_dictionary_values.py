import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_dictionary_values(dictionary, to_language):
    credential = TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY'))
    client = TextTranslationClient(endpoint=f'https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com/', credential=credential)
    texts = list(dictionary.values())
    result = client.translate(texts, to_language)
    return {key: translation.translations[0].text for key, translation in zip(dictionary.keys(), result)}

if __name__ == '__main__':
    dictionary = {'greeting': 'Hello, world!', 'question': 'How are you?'}
    print(translate_dictionary_values(dictionary, 'es'))