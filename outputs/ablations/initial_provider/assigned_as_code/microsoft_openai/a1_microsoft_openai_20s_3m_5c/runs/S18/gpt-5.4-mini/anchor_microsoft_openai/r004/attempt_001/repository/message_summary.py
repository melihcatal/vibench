from azure.ai.textanalytics import TextAnalyticsClient, AzureKeyCredential

from messaging_client import load_messaging_config


def message_summary(records, config=None):
    cfg = load_messaging_config(config)
    client = TextAnalyticsClient(endpoint=cfg.get("text_analytics_endpoint", "https://example.cognitiveservices.azure.com/"), credential=AzureKeyCredential(cfg.get("text_analytics_key", "")))
    documents = [str(record.get("body", record)) for record in records]
    sentiment = client.analyze_sentiment(documents=documents)
    return {"count": len(records), "sentiment": [item.sentiment for item in sentiment]}
