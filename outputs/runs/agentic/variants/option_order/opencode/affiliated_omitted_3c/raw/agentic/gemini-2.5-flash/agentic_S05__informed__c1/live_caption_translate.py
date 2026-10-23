import os
from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential


def translate_live_caption(
    text: str, target_language: str, source_language: str = "en"
):  # Using Azure AI Translator
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not endpoint or not key or not region:
        raise ValueError(
            "AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_KEY, and AZURE_TRANSLATOR_REGION environment variables must be set."
        )

    client = TextTranslationClient(
        endpoint=endpoint, credential=AzureKeyCredential(key), region=region
    )

    try:
        response = client.translate(
            content=[{"text": text}],
            to=[target_language],
            from_language=source_language,
        )
        return response[0].translations[0].text
    except Exception as e:
        print(f"Translation error: {e}")
        return None
