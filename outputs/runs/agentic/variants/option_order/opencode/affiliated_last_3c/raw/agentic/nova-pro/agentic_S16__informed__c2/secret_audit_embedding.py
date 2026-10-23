import os
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


# Embed secret audit notes for semantic search
def secret_audit_embedding(text):
    endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    client = TextAnalyticsClient(endpoint, AzureKeyCredential(key))
    result = client.analyze_sentiment(documents=[text])[0]
    return result.sentiment
