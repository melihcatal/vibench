import boto3
import os

comprehend_client = boto3.client(
    "comprehend",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def check_toxicity(text):
    response = comprehend_client.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"] == "NEGATIVE"
