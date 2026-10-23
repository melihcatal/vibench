import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(endpoint=os.getenv('AZURE_TEXT_ANALYTICS_ENDPOINT'), credential=AzureKeyCredential(os.getenv('AZURE_TEXT_ANALYTICS_KEY')))

def summarize_metric(text):
    result = client.summarize(documents=[text])
    return result[0].sentences
