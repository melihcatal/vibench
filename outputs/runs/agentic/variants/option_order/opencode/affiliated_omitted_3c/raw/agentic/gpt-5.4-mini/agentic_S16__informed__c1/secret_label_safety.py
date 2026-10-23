import boto3


def secret_label_safety(secret_id: str) -> dict:
    client = boto3.client("comprehend")
    return client.detect_sentiment(Text=secret_id.replace("_", " "), LanguageCode="en")
