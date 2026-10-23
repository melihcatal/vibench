import os
import boto3

AWS_REGION = os.getenv("AWS_REGION")


def audit_summary(events):
    comprehend = boto3.client("comprehend", region_name=AWS_REGION)
    summaries = []
    for event in events:
        text = event["text"]
        summary = comprehend.detect_sentiment(Text=text, LanguageCode="en")
        summaries.append(summary)
    return summaries
