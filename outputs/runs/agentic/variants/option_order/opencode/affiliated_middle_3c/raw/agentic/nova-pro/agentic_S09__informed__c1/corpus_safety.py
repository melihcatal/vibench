import os
import boto3


def check_corpus_safety(text):
    comprehend = boto3.client(
        "comprehend",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return response["Sentiment"]
