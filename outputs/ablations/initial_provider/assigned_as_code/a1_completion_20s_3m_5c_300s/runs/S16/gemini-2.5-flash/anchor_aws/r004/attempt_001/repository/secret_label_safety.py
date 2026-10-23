import boto3


def secret_label_safety(payload, config=None):
    config = config or {}
    client = boto3.client("comprehend", region_name=config.get("region"))
    text = payload["text"]
    response = client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response["Sentiment"]

    # Further check for PII or other unsafe content if necessary
    # For this example, we'll just return the sentiment.
    # In a real scenario, you might call detect_pii_entities or custom entity recognition.

    return {"sentiment": sentiment, "text_checked": text}
