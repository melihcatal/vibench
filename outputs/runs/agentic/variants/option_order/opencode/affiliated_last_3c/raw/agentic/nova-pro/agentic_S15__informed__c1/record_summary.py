import os
import boto3
from botocore.exceptions import NoCredentialsError


def record_summary(text):
    comprehend = boto3.client("comprehend")
    try:
        summary = comprehend.detect_sentiment(Text=text, LanguageCode="en")
        return summary
    except NoCredentialsError:
        return "No AWS credentials found"
