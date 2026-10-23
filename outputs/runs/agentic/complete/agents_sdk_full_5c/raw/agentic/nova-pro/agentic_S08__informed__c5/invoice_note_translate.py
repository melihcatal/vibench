import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

credential = TranslatorCredential(os.getenv('AZURE_TRANSLATOR_KEY'))
client = TextTranslationClient(endpoint=f'https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsofttranslator.com', credential=credential)

def translate_invoice_note(note, target_language='es'):
    result = client.translate([note], target_language)[0]
    return result.translations[0].text