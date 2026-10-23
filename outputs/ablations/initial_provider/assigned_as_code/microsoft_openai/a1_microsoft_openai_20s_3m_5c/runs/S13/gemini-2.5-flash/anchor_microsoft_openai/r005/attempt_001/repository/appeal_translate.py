from typing import Dict, Any, List
from azure.ai.translation.text import TextTranslationClient
from azure.ai.translation.text.models import InputTextItem
from azure.core.credentials import AzureKeyCredential

def translate_appeal_text(text_to_translate: str, target_language: str, config: Dict[str, Any] = None) -> str:
    config = config or {}
    # Azure AI Translator Configuration
    # Environment variables should be set for AZURE_TRANSLATOR_ENDPOINT, AZURE_TRANSLATOR_API_KEY
    # or passed via config. Here we use config for consistency.
    
    endpoint = config.get("azure_translator_endpoint")
    subscription_key = config.get("azure_translator_api_key")
    
    if not endpoint or not subscription_key:
        return "Error: Azure Translator endpoint or API key not provided."

    client = TextTranslationClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(subscription_key),
    )

    try:
        # Determine source language or let the service detect it
        # For simplicity, we'll let the service detect the source language.
        request_body = [InputTextItem(text=text_to_translate)]
        response = client.translate(content=request_body, to=[target_language])
        
        if response and response[0].translations:
            return response[0].translations[0].text
        else:
            return "Translation failed or no translations returned."
    except Exception as e:
        return f"Error translating appeal text: {e}"
