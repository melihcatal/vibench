import json
from model_client import ManagedModelClient
from google.cloud import translate_v2 as translate


def localized_platform_output(provider_output: str, target_locale: str) -> dict:
    """Translate the model's text response to another locale using Google Cloud Translation.

    Returns the translated text together with the original metadata.
    """
    client = translate.Client()
    translation = client.translate(provider_output, target_language=target_locale)
    return {
        "translated_output": translation["translatedText"],
        "original_output": provider_output,
        "metadata": {"locale": target_locale},
    }
