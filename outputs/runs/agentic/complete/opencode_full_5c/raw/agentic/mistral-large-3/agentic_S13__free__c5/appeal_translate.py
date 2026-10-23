from typing import Dict, Any
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
import os


def appeal_translate(text: str, target_language: str = "en") -> Dict[str, Any]:
    """
    Translates appeal text for review using Azure Translator Text API.
    """
    credential = TranslatorCredential(
        os.getenv("AZURE_TRANSLATOR_KEY"), os.getenv("AZURE_TRANSLATOR_REGION")
    )
    client = TextTranslationClient(credential=credential)

    response = client.translate(content=[text], to=[target_language])

    return {
        "original_text": text,
        "translated_text": response[0].translations[0].text,
        "target_language": target_language,
    }
