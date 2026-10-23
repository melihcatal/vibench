import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_dictionary_values(dictionary, to_language):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(
        endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com/",
        credential=credential,
    )
    translated_values = {}
    for key, value in dictionary.items():
        result = client.translate([value], to_language)[0]
        translated_values[key] = result.translations[0]
    return translated_values


if __name__ == "__main__":
    print(translate_dictionary_values({"greeting": "Hello, world!"}, "es"))
