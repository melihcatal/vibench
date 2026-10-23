from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def incident_summary(payload, config=None):
    config = config or {}
    texts = payload["messages"]
    client = TextAnalyticsClient(endpoint=config["endpoint"], credential=AzureKeyCredential(config["key"]))
    result = client.analyze_sentiment(texts)
    return {"summaries": [getattr(item, "sentiment", None) for item in result]}
