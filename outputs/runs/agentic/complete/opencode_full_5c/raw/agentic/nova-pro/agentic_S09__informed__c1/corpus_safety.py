import os
import boto3

aws_access_key_id = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.getenv("AWS_SECRET_ACCESS_KEY")

comprehend = boto3.client(
    "comprehend",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name="us-west-2",
)


def check_corpus_safety(text):
    response = comprehend.detect_toxic_content(TextSegments=[text])
    return response["Results"][0]["Toxicity"]
