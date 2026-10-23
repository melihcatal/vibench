import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential


def batch_translate(texts, to_language):
    credential = TranslatorCredential(os.getenv("AZURE_TRANSLATOR_KEY"))
    client = TextTranslationClient(
        endpoint=f"https://{os.getenv('AZURE_TRANSLATOR_REGION')}.api.cognitive.microsoft.com/",
        credential=credential,
    )
    results = client.translate(texts, to_language)
    return [result.translations[0] for result in results]


if __name__ == "__main__":
    print(batch_translate(["Hello, world!", "Goodbye!"], "es"))
