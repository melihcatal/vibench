from typing import Dict, Any
import requests
from .model_client import get_model_client_config
from .model_models import ChatResponse


def localized_platform_output(
    response: ChatResponse,
    target_locale: str = "es",
    api_key: Optional[str] = None,
) -> ChatResponse:
    """
    Translates Azure AI Inference model output using Azure Translator.
    """
    config = get_model_client_config()
    api_key = api_key or config.get("AZURE_TRANSLATOR_KEY")
    endpoint = config.get(
        "AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com"
    )

    if not api_key:
        raise ValueError("Missing required configuration for Azure Translator.")

    headers = {
        "Ocp-Apim-Subscription-Key": api_key,
        "Ocp-Apim-Subscription-Region": config.get("AZURE_TRANSLATOR_REGION", "global"),
        "Content-Type": "application/json",
    }

    payload = [{"text": response.content}]

    translate_response = requests.post(
        f"{endpoint}/translate?api-version=3.0&to={target_locale}",
        headers=headers,
        json=payload,
    )
    translate_response.raise_for_status()

    translated_text = translate_response.json()[0]["translations"][0]["text"]

    return ChatResponse(
        content=translated_text,
        finish_reason=response.finish_reason,
        usage=response.usage,
    )
