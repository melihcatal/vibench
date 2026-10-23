import os
import boto3
from botocore.exceptions import NoCredentialsError


def log_text_safety(log_message):
    client = boto3.client("comprehend", region_name="us-west-2")
    try:
        response = client.detect_toxic_content(TextSegments=[{"Text": log_message}])
        return response["Results"][0]["Toxicity"]
    except NoCredentialsError:
        return "No AWS credentials found"
