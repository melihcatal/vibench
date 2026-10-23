import boto3


def moderate_transcript(payload, config=None):
    client = boto3.client("comprehend", region_name=(config or {}).get("region"))
    response = client.detect_sentiment(Text=payload["text"], LanguageCode=payload.get("language_code", "en"))
    return {"sentiment": response["Sentiment"], "sentiment_score": response["SentimentScore"]}
