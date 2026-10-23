from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class EmbeddingClient:
    def __init__(self, endpoint, key):
        self.client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))

    def embed(self, text):
        result = self.client.extract_key_phrases(text)
        return result.key_phrases