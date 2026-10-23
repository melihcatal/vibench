from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_ocr_text(
    text: str, target_language: str, source_language: str | None = None
) -> str:
    client = TextTranslationClient(
        endpoint="https://api.cognitive.microsofttranslator.com",
        credential=AzureKeyCredential(
            __import__("os").getenv("AZURE_TRANSLATOR_KEY", "")
        ),
        region=__import__("os").getenv("AZURE_TRANSLATOR_REGION", ""),
    )
    result = client.translate(
        content=[text], to=[target_language], from_parameter=source_language
    )
    return result[0].translations[0].text if result and result[0].translations else ""
