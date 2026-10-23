from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_markup(text, target_lang):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(
        endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsofttranslator.com",
        credential=credential,
    )
    result = client.translate(text, to=[target_lang])[0].translations[0].text
    return result
