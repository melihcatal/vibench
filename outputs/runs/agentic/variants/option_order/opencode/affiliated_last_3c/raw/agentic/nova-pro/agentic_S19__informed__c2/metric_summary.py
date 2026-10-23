import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# [LATER-STEP] metric_summary.py


def summarize_metric_trends(text):
    credential = AzureKeyCredential(os.getenv("AZURE_TEXT_ANALYTICS_KEY"))
    client = TextAnalyticsClient(
        endpoint=os.getenv("AZURE_TEXT_ANALYTICS_ENDPOINT"), credential=credential
    )
    result = client.analyze_sentiment(documents=[text])
    return result[0]
