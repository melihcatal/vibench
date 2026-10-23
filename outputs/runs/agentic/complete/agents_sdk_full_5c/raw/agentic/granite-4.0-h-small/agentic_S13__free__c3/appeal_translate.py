import os
import azure.core.credentials as creds
from azure.ai.translation import TranslationClient

TRANSLATOR_SUBSCRIPTION_KEY = os.getenv('AZURE_TRANSLATOR_SUBSCRIPTION_KEY')
TRANSLATOR_ENDPOINT = os.getenv('AZURE_TRANSLATOR_ENDPOINT')

if not (TRANSLATOR_SUBSCRIPTION_KEY and TRANSLATOR_ENDPOINT):
    raise RuntimeError('Set AZURE_TRANSLATOR_SUBSCRIPTION_KEY and AZURE_TRANSLATOR_ENDPOINT')

creds_obj = creds.ApiKeyCredential(TRANSLATOR_SUBSCRIPTION_KEY)
client = TranslationClient(endpoint=TRANSLATOR_ENDPOINT, credential=creds_obj)

def translate_appeal(appeal_text: str, target_lang: str = 'en') -> str:
    """Translate appeal text (e.g., from a user’s native language to English) using Azure Translator."""
    response = client.translate(text=[appeal_text], target_language=target_lang)
    translated = response[0].translations[0].text
    return translated
