import os
import boto3

comprehend = boto3.client("comprehend", region_name="us-west-2")


def check_safety(text):
    response = comprehend.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    return response["Results"][0]["Toxicity"]
