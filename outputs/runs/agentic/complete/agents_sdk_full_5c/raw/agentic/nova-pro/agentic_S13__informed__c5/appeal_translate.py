from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

credential = TranslatorCredential('AZURE_TRANSLATOR_KEY', 'AZURE_TRANSLATOR_REGION')
client = TextTranslationClient(credential=credential)

def appeal_translate(text, to_language='es'):
    result = client.translate([text], to_language)
    return result[0].translations[0].text
