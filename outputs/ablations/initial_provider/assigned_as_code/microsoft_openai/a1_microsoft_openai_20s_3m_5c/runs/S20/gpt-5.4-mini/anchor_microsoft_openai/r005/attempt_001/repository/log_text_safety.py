from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential


def log_text_safety(payload, config=None):
    config = config or {}
    client = TextAnalyticsClient(endpoint=config["endpoint"], credential=AzureKeyCredential(config["key"]))
    result = client.analyze_sentiment([payload["text"]])[0]
    unsafe = result.confidence_scores.negative > 0.85 or payload.get("contains_secret", False)
    return {"unsafe": unsafe, "sentiment": result.sentiment}
