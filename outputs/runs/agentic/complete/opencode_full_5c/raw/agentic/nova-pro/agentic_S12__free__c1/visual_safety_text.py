import boto3

client = boto3.client("comprehend")


def visual_safety_text(text):
    response = client.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"] == "NEGATIVE"
