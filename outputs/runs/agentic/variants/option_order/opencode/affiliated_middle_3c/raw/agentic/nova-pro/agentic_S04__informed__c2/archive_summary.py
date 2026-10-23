import os
from azure.ai.textanalytics import TextAnalyticsClient, AzureKeyCredential


def archive_summary(transcript):
    key = os.getenv("AZURE_TEXT_ANALYTICS_KEY")
    endpoint = os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT")
    credential = AzureKeyCredential(key)
    client = TextAnalyticsClient(endpoint, credential)
    result = client.summarize(transcript)[0]
    return result.sentences[0].text
