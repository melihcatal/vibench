import os

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_script(
    text: str, target_language: str, source_language: str = None
) -> str:
    client = TextTranslationClient(
        endpoint=os.environ.get(
            "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
        ),
        credential=AzureKeyCredential(os.environ.get("AZURE_TRANSLATOR_KEY", "")),
        region=os.environ.get("AZURE_TRANSLATOR_REGION", ""),
    )
    result = client.translate(
        content=[text], to=[target_language], from_parameter=source_language
    )
    return result[0].translations[0].text
