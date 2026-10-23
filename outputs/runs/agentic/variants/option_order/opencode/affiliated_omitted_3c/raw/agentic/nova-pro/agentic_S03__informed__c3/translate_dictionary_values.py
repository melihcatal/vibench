import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_dictionary_values(dictionary, source_lang, target_lang):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(
        endpoint="https://api.cognitive.microsofttranslator.com/", credential=credential
    )
    translated_dict = {}
    for key, value in dictionary.items():
        result = client.translate(value, to=[target_lang], from_parameter=source_lang)
        translated_dict[key] = result[0].translations[0].text
    return translated_dict
