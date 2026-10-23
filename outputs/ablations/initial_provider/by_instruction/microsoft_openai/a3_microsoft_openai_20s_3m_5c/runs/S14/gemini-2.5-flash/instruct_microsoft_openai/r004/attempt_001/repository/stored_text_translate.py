import os
from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.ai.translation.text.models import InputTextItem

def translate_stored_text(text: str, target_language: str, source_language: str | None = None) -> str:
    """
    Translates text extracted from a stored document using Azure AI Translator.

    Args:
        text (str): The text to translate.
        target_language (str): The language code to translate the text into (e.g., "es" for Spanish).
        source_language (str | None): The language code of the input text (e.g., "en" for English).
                                    If None, the service will attempt to auto-detect.

    Returns:
        str: The translated text.
    """
    endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    key = os.environ.get("AZURE_TRANSLATOR_KEY")
    region = os.environ.get("AZURE_TRANSLATOR_REGION") # Optional, but good for some setups

    if not endpoint or not key:
        raise ValueError("AZURE_TRANSLATOR_ENDPOINT and AZURE_TRANSLATOR_KEY environment variables must be set.")

    credential = TranslatorCredential(key, region)
    client = TextTranslationClient(endpoint=endpoint, credential=credential)

    input_text_items = [InputTextItem(text=text)]
    if source_language:
        response = client.translate(content=input_text_items, to=[target_language], from_parameter=source_language)
    else:
        response = client.translate(content=input_text_items, to=[target_language])

    if response and response[0].translations:
        return response[0].translations[0].text
    else:
        return "Translation failed or no translation found."
