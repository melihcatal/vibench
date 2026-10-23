import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

class AzureModelClient:
    def __init__(self):
        self.endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
        self.key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')
        self.client = TextAnalyticsClient(endpoint=self.endpoint, credential=AzureKeyCredential(self.key))

    def invoke_model(self, model_id, input_text):
        response = self.client.analyze_sentiment(documents=[input_text])[0]
        return response

    def select_resource(self, model_id):
        return model_id

    def stream_generation(self, model_id, input_text):
        response = self.client.analyze_sentiment(documents=[input_text])[0]
        yield response

    def collect_metadata(self, model_id, input_text):
        response = self.client.analyze_sentiment(documents=[input_text])[0]
        metadata = {'model_id': model_id, 'usage': 'sentiment analysis'}
        return response, metadata