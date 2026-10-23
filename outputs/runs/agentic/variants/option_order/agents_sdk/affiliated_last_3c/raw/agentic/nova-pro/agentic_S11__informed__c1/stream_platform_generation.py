import os
from azure.ai.textanalytics import TextAnalyticsClient, TextAnalyticsApiKeyCredential

endpoint = os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT')
key = os.getenv('AZURE_TEXT_ANALYTICS_KEY')

client = TextAnalyticsClient(endpoint=endpoint, credential=TextAnalyticsApiKeyCredential(key))

def stream_generation(text):
    response = client.analyze_sentiment(documents=[text])
    for document in response:
        yield document
