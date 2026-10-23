import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_text(text, to_language):
    credential = TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY'))
    client = TextTranslationClient(endpoint=f'https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com/', credential=credential)
    result = client.translate([text], to_language)
    return result[0].translations[0].text

if __name__ == '__main__':
    print(translate_text('Hello, world!', 'es'))