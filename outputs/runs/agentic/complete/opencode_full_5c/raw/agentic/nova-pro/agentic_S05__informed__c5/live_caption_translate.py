import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential

os.environ["AZURE_TRANSLATOR_KEY"] = "your-translator-key"
os.environ["AZURE_TRANSLATOR_REGION"] = "your-translator-region"


def translate_text(text, target_language):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(credential, os.getenv("AZURE_TRANSLATOR_REGION"))
    result = client.translate([text], target_language)[0]
    return result.translations[0].text


if __name__ == "__main__":
    print(translate_text("Hello, world!", "es"))
