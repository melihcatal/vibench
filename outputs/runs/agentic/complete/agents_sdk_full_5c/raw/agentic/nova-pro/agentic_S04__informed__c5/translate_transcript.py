import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

translation_key = os.getenv('AZURE_TRANSLATOR_KEY')
translation_region = os.getenv('AZURE_TRANSLATOR_REGION')

def translate_transcript(transcript, target_language='es'):
    credential = TranslatorCredential(translation_key)
    client = TextTranslationClient(credential, translation_region)
    result = client.translate([transcript], target_language)[0]
    return result.translations[0].text