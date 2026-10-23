import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_invoice_note(note, to_language='en'):
    credential = TranslatorCredential(os.getenv('TRANSLATOR_KEY'))
    client = TextTranslationClient(endpoint='https://api.cognitive.microsofttranslator.com/', credential=credential)
    result = client.translate([note], to_language)[0]
    return result.translations[0].text