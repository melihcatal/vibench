import boto3

from vision_client import load_vision_config


def visual_safety_text(payload, config=None):
    config = load_vision_config(config)
    client = boto3.client("comprehend", region_name=config.get("region"))
    response = client.detect_sentiment(Text=payload["text"], LanguageCode=payload.get("language", "en"))
    return {"sentiment": response.get("Sentiment", "NEUTRAL")}
