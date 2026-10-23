import os
import boto3

comprehend = boto3.client("comprehend")


def check_text_safety(text):
    result = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    return result["Sentiment"] != "NEGATIVE"
