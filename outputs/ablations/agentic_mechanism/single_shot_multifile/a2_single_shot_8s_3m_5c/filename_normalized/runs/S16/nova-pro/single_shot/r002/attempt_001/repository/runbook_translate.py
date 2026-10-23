import os
from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput
from azure.core.credentials import AzureKeyCredential

def runbook_translate(text, to_language):
    endpoint = os.getenv('AZURE_TRANSLATOR_ENDPOINT')
    key = os.getenv('AZURE_TRANSLATOR_KEY')
    client = DocumentTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))
    input = DocumentTranslationInput(source_url=None, target_url=None, target_language_code=to_language)
    poller = client.start_translation(input)
    result = poller.result()
    return result[0].translated_document.content