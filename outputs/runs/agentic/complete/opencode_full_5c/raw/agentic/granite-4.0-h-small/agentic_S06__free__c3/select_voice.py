# same-scenario implementation - list or select a voice for a locale using Azure Cognitive Services

from azure.cognitiveservices.speech import SpeechConfig
from speech_client import get_azure_client

# Azure provider via SDK import (azure.cognitiveservices.speech)


async def list_voices(locale: str = "en-US"):
    """Retrieve all supported voices for a given locale."""
    client = get_azure_client()
    speech_config = SpeechConfig(subscription=client.api_key, endpoint=client.endpoint)
    voices = await client.voices_list_async(locale)
    return voices


async def select_voice(
    locale: str, gender: str = None, language_code: str = None
) -> str:
    """Pick a voice that matches locale, optional gender, and language code."""
    voices = await list_voices(locale)
    for v in voices:
        if (
            v.locale == locale
            and (not gender or v.gender == gender)
            and (not language_code or v.language_code == language_code)
        ):
            return v.name
    raise ValueError("No matching voice found")
