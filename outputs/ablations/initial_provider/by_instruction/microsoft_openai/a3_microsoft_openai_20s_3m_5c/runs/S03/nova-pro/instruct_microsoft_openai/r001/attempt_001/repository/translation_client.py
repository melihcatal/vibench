import os
from azure.ai.translation.document.aio import DocumentTranslationClient
from azure.core.credentials import AzureKeyCredential

class TranslationClient:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_TRANSLATION_ENDPOINT')
        self.key = os.getenv('AZURE_TRANSLATION_KEY')
        self.credential = AzureKeyCredential(self.key)
        self.client = DocumentTranslationClient(self.endpoint, self.credential)