from azure.identity import DefaultAzureCredential
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient
import os

def get_key_vault_url():
    key_vault_url = os.environ.get("KEY_VAULT_URL")
    if not key_vault_url:
        raise ValueError("KEY_VAULT_URL environment variable not set.")
    return key_vault_url

def get_key_client():
    key_vault_url = get_key_vault_url()
    credential = DefaultAzureCredential()
    return KeyClient(vault_url=key_vault_url, credential=credential)

def get_cryptography_client(key_id):
    credential = DefaultAzureCredential()
    return CryptographyClient(key_id=key_id, credential=credential)

def get_text_analytics_client():
    from azure.core.credentials import AzureKeyCredential
    from azure.ai.textanalytics import TextAnalyticsClient
    text_analytics_endpoint = os.environ.get("TEXT_ANALYTICS_ENDPOINT")
    text_analytics_key = os.environ.get("TEXT_ANALYTICS_KEY")
    if not text_analytics_endpoint or not text_analytics_key:
        raise ValueError("TEXT_ANALYTICS_ENDPOINT and TEXT_ANALYTICS_KEY environment variables must be set.")
    return TextAnalyticsClient(endpoint=text_analytics_endpoint, credential=AzureKeyCredential(text_analytics_key))

def get_translator_client():
    from azure.ai.translation.text import TextTranslationClient
    from azure.ai.translation.text.models import TextTranslationInput
    from azure.core.credentials import AzureKeyCredential
    translator_endpoint = os.environ.get("TRANSLATOR_ENDPOINT")
    translator_key = os.environ.get("TRANSLATOR_KEY")
    translator_region = os.environ.get("TRANSLATOR_REGION")
    if not translator_endpoint or not translator_key or not translator_region:
        raise ValueError("TRANSLATOR_ENDPOINT, TRANSLATOR_KEY, and TRANSLATOR_REGION environment variables must be set.")
    return TextTranslationClient(endpoint=translator_endpoint, credential=AzureKeyCredential(translator_key), region=translator_region)
