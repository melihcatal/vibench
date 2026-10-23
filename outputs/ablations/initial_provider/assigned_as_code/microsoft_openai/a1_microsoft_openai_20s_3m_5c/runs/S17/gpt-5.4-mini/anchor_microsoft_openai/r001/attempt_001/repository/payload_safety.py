from azure.identity import DefaultAzureCredential
from azure.ai.textanalytics import TextAnalyticsClient

from security_models import normalize_text


def payload_safety(payload=None, config=None):
    payload = payload or {}
    config = config or {}
    text = normalize_text(payload.get("plaintext"))
    with DefaultAzureCredential() as credential:
        client = TextAnalyticsClient(endpoint=config["endpoint"], credential=credential)
        analysis = client.analyze_sentiment([text])[0]
    return {"unsafe": analysis.confidence_scores.negative > 0.5, "sentiment": analysis.sentiment, "text": text}
