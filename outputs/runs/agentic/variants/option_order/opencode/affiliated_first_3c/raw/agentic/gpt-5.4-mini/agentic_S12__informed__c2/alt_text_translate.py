from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def alt_text_translate(text: str, target_language: str) -> str:
    client = TextTranslationClient(
        endpoint="https://api.cognitive.microsofttranslator.com",
        credential=AzureKeyCredential(__import__("os").environ["AZURE_TRANSLATOR_KEY"]),
    )
    result = client.translate(content=[text], to=[target_language])
    return result[0].translations[0].text if result and result[0].translations else ""


__all__ = ["alt_text_translate"]
