import os

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

import boto3

client = boto3.client(
    "comprehend",
    region_name="us-west-2",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)


def safety_threshold(text):
    response = client.detect_sentiment(Text=text, LanguageCode="en")
    sentiment = response["Sentiment"]
    if sentiment == "NEGATIVE":
        return False
    return True
