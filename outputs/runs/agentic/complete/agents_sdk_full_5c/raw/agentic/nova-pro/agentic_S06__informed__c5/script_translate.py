from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

def translate_script(text, to_language):
    credential = TranslatorCredential('AZURE_TRANSLATOR_KEY')
    client = TextTranslationClient(endpoint='https://api.cognitive.microsofttranslator.com/', credential=credential)
    result = client.translate([text], to_language)[0]
    return result.translations[0].text