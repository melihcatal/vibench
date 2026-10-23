import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class EmbeddingsClient:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
        self.key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
        self.credentials = AzureKeyCredential(self.key)
        self.client = TextAnalyticsClient(endpoint=self.endpoint, credential=self.credentials)

    def get_text_analytics_client(self):
        return self.client