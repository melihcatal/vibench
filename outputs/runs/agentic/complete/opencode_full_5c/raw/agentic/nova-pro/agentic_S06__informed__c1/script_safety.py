import boto3


def check_script_safety(text):
    comprehend = boto3.client("comprehend")
    result = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return result.get("Sentiment")
