import os
from azure.ai.translation.text import TranslatorClient
from azure.core.credentials import AzureKeyCredential


# Translate secret-rotation runbook notes
def runbook_translate(text, to_language):
    endpoint = os.getenv("AZURE_TRANSLATOR_ENDPOINT")
    key = os.getenv("AZURE_TRANSLATOR_KEY")
    client = TranslatorClient(endpoint, AzureKeyCredential(key))
    result = client.translate(content=[text], to=to_language)[0]
    return result.translations[0].text
