import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def translate_markup(text, to_language):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(
        endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com/",
        credential=credential,
    )
    result = client.translate([text], to_language)[0]
    return result.translations[0]


if __name__ == "__main__":
    print(translate_markup("<p>Hello, world!</p>", "es"))
