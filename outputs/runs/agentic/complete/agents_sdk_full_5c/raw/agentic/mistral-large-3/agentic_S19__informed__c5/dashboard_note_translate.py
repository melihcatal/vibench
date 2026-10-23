from azure.ai.translation.text import TextTranslationClient, TranslatorCredential
from azure.core.exceptions import AzureError
from observability_client import get_client_config


def translate_dashboard_note(text: str, target_language: str = "es") -> str:
    config = get_client_config()
    key = config.get("AZURE_TRANSLATOR_KEY")
    region = config.get("AZURE_TRANSLATOR_REGION")
    
    if not key or not region:
        raise ValueError("AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION environment variables are required.")
    
    credential = TranslatorCredential(key, region)
    client = TextTranslationClient(credential=credential)
    
    try:
        response = client.translate(content=[text], to=[target_language])
        return response[0].translations[0].text
    except AzureError as e:
        raise RuntimeError(f"Translation failed: {e}")