from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class SummaryClient:
    def __init__(self, endpoint, key):
        self.client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))

    def summarize(self, text):
        result = self.client.summarize(text)
        return result[0].sentences[0].text