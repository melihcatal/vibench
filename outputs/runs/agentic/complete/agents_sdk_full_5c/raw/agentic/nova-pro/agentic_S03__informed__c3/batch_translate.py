import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def batch_translate(texts, to_language):
    credential = TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY'))
    client = TextTranslationClient(endpoint=f'https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com/', credential=credential)
    result = client.translate(texts, to_language)
    return [item.translations[0].text for item in result]

if __name__ == '__main__':
    texts = ['Hello, world!', 'How are you?']
    print(batch_translate(texts, 'es'))