import os
import boto3

client = boto3.client(
    "comprehend",
    region_name="us-west-2",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
)


def check_safety(text):
    response = client.detect_toxic_content(
        TextSegments=[{"Text": text}], LanguageCode="en"
    )
    return response["ResultList"][0]["Toxicity"]
