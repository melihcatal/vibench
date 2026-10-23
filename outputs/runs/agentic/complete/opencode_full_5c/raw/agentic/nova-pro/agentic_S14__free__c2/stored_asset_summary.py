import boto3


def stored_asset_summary(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    print(f"Sentiment analysis: {response}")
    return response
