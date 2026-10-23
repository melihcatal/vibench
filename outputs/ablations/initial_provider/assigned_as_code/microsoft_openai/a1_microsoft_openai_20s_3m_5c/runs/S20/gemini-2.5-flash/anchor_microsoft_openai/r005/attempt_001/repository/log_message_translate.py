import os
from typing import List
from observability_client import get_translator_client
from observability_models import TranslatedMessage


def translate_log_message(log_message: str, target_locale: str) -> TranslatedMessage:
    translator_endpoint = os.environ.get("AZURE_TRANSLATOR_ENDPOINT")
    translator_key = os.environ.get("AZURE_TRANSLATOR_KEY")
    translator_region = os.environ.get("AZURE_TRANSLATOR_REGION")

    if not all([translator_endpoint, translator_key, translator_region]):
        raise ValueError("Missing Azure Translator configuration: endpoint, key, or region.")

    client = get_translator_client(translator_endpoint, translator_region, translator_key)

    response = client.translate_text(
        body=[{"text": log_message}],
        to=[target_locale]
    )
    
    # The response is a list of dictionaries. Each dictionary contains a 'translations' key,
    # which is another list of dictionaries. We expect one translation for one message.
    translated_text = response[0]['translations'][0]['text']

    return TranslatedMessage(translated_text=translated_text, target_locale=target_locale)
