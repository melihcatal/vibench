from typing import Dict, Any
from model_models import ChatResponse
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem
import os


def translate_platform_output(
    response: ChatResponse,
    target_language: str = "es",
) -> Dict[str, Any]:
    """
    Translates Azure AI Inference model output to another locale using Azure Translator.
    """
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    region = os.getenv("AZURE_TRANSLATOR_REGION")

    if not all([key, endpoint, region]):
        raise ValueError("Missing required Azure Translator configuration.")

    client = TextTranslationClient(
        credential=TranslatorCredential(key, region),
        endpoint=endpoint,
    )

    input_text_elements = [InputTextItem(text=response.content)]
    response = client.translate(
        content=input_text_elements,
        to=[target_language],
    )

    translation = response[0] if response else None
    translated_text = (
        translation.translations[0].text
        if translation and translation.translations
        else ""
    )

    return {
        "original_text": response.content,
        "translated_text": translated_text,
        "target_language": target_language,
        "raw_response": response,
    }
