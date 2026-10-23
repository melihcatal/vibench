import boto3


def moderate_vendor_text(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response["Sentiment"]
    if sentiment == "NEGATIVE":
        return "Moderated"
    return text
