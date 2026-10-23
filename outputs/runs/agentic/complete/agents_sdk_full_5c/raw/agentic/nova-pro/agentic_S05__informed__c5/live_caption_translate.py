import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

translation_client = TextTranslationClient(endpoint='https://api.cognitive.microsofttranslator.com/', credential=TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY')))

def translate_text(text, to_language='es'):
    result = translation_client.translate(text, to_language)
    return result[0].text