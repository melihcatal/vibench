import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_text(text, target_language='en'):
    client = TextTranslationClient(endpoint=os.getenv('AZURE_TRANSLATION_ENDPOINT'), credential=TranslatorCredential(os.getenv('AZURE_TRANSLATION_KEY')))
    result = client.translate([text], target_language)[0]
    return result.translations[0].text