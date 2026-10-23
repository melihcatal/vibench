import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_dictionary_values(dictionary, from_language, to_language):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(credential, os.getenv("AZURE_TRANSLATOR_REGION"))
    texts = list(dictionary.values())
    result = client.translate(texts, from_language, to_language)
    translated_dict = {
        key: translation.translations[0].text
        for key, translation in zip(dictionary.keys(), result)
    }
    return translated_dict
