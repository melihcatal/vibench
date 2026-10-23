import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_text(text, to_language):
    credential = TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY'))
    client = TextTranslationClient(endpoint=f'https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsofttranslator.com', credential=credential)
    result = client.translate(text, to_language)[0]
    return result.translations[0].text