from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_invoice_note(note, target_language='en'):
    credential = TranslatorCredential('YOUR_API_KEY')
    client = TextTranslationClient(endpoint='https://api.cognitive.microsofttranslator.com/', credential=credential)
    result = client.translate([note], target_language)[0]
    return result.translations[0].text