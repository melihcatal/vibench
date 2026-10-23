import json

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_payload(text: str, target_language: str) -> dict:
    client = TextTranslationClient(endpoint=os.environ["AZURE_TRANSLATOR_ENDPOINT"], credential=AzureKeyCredential(os.environ["AZURE_TRANSLATOR_KEY"]))
    response = client.translate(content=[text], to=[target_language])
    return {"translated": response[0].translations[0].text}


if __name__ == "__main__":
    import os
    print(json.dumps(translate_payload("hello", "es")))
