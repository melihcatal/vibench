import os
from azure.ai.translation.text import TextTranslationClient, TextTranslationApiKeyCredential

def translate_invoice_note(note, target_language='en'):
    client = TextTranslationClient(
        endpoint=os.getenv('TRANSLATION_ENDPOINT'),
        credential=TextTranslationApiKeyCredential(os.getenv('TRANSLATION_KEY'))
    )
    result = client.translate([note], target_language)[0]
    return result.translations[0].text