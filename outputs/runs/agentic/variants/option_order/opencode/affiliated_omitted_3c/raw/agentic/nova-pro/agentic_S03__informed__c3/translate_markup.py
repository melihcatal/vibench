import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_markup(markup, source_lang, target_lang):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(
        endpoint="https://api.cognitive.microsofttranslator.com/", credential=credential
    )
    result = client.translate(markup, to=[target_lang], from_parameter=source_lang)
    return result[0].translations[0].text
