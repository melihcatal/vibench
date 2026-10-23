import json
from typing import List

from azure.core.credentials import AzureKeyCredential
from azure.ai.translation import DocumentTranslationClient

from security_client import get_config
from security_models import SecretDef

def runbook_translate(secret_def: SecretDef, runbook_note: str) -> str:
    """Translate secret-rotation runbook notes using Azure AI Translator.
    Returns the translated English text.
    """
    endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    key = os.getenv('AZURE_TRANSLATOR_KEY')
    if not endpoint or not key:
        raise RuntimeError('Azure Translator credentials not set')
    client = DocumentTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    source = runbook_note
    translation = client.translate_documents(texts=[source], target_language_code='en',
                                             document_type='text/plain')
    translated = translation.translated_documents[0].translations[0].content
    return translated.strip()
