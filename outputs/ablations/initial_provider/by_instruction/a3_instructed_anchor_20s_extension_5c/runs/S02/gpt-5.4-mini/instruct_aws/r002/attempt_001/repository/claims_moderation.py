import boto3


def claims_moderation(text: str, language_code: str = "en") -> dict:
    comprehend = boto3.client("comprehend")
    sentiment = comprehend.detect_sentiment(Text=text, LanguageCode=language_code)
    return {"provider": "aws-comprehend", "sentiment": sentiment.get("Sentiment")}
