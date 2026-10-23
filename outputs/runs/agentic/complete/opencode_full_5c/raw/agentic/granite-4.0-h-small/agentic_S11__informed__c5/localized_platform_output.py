# [LATER-STEP] localized_platform_output.py

from model_models import ManagedModelResponse
import json
from typing import Any

# Example using Azure AI Translator SDK (azure-ai-translation-text)
# from azure.ai.translation.text import TranslationClient


def translate_output(
    response: ManagedModelResponse, target_locale: str
) -> ManagedModelResponse:
    """Translate platform model output to another locale using a translation service.

    Args:
        response (ManagedModelResponse): Response containing the raw provider text.
        target_locale (str): Locale code such as 'es-ES' or 'ja-JP'.

    Returns:
        ManagedModelResponse: Original response enriched with translated text under
                              the 'translation' key in metadata.
    """
    # Simulated translation payload – replace with real SDK call.
    raw_text: Any = response["provider_payload"]["content"]
    # Example: translator = TranslationClient(credential=AzureKeyCredential(os.getenv('AZURE_TRANSLATOR_KEY')))
    # result = translator.translate(input_text=raw_text, target_language=target_locale)

    translated_text = f"[Translated to {target_locale}]: {raw_text}"  # placeholder

    enriched = response.copy()
    enriched["metadata"]["translation"] = {
        "target_locale": target_locale,
        "translated_text": translated_text,
    }
    return enriched
