import os
from azure.ai.translation.document import DocumentTranslationClient, DocumentTranslationInput
from azure.core.credentials import AzureKeyCredential

endpoint = os.getenv('AZURE_TRANSLATE_ENDPOINT')
key = os.getenv('AZURE_TRANSLATE_KEY')
client = DocumentTranslationClient(endpoint=endpoint, credential=AzureKeyCredential(key))

def translate_runbook_notes(notes, target_language='es'):
    input = DocumentTranslationInput(source_url=notes, target_language_code=target_language)
    poller = client.begin_translate_document(input)
    result = poller.result()
    return result.translations[0].content