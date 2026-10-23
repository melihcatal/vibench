import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class ModelClient:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
        self.key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
        self.client = TextAnalyticsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))

    def get_client(self):
        return self.client