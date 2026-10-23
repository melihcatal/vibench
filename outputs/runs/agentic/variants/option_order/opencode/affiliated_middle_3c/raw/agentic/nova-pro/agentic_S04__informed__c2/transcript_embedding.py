import os
from azure.ai.textanalytics import TextAnalyticsClient, AzureKeyCredential


def transcript_embedding(transcript):
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint, credential)
    result = client.extract_key_phrases(transcript)[0]
    return result.key_phrases
