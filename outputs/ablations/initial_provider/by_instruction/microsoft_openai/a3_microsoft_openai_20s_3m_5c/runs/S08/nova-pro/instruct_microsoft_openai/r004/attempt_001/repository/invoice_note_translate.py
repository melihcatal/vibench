from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import TextTranslationInput

def translate_invoice_note(note, target_language='en'):
    endpoint = os.getenv('TRANSLATION_ENDPOINT')
    key = os.getenv('TRANSLATION_KEY')
    client = TextTranslationClient(endpoint, AzureKeyCredential(key))
    result = client.translate([TextTranslationInput(text=note, target_language_code=target_language)])
    translated_note = result[0].translations[0].text
    return translated_note