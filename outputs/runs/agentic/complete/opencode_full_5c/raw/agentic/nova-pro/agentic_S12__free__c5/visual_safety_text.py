import boto3


def check_unsafe_text(labels):
    comprehend_client = boto3.client("comprehend")
    for label in labels:
        response = comprehend_client.detect_sentiment(
            Text=label["Name"], LanguageCode="en"
        )
        if response["Sentiment"] == "NEGATIVE":
            return True
    return False
