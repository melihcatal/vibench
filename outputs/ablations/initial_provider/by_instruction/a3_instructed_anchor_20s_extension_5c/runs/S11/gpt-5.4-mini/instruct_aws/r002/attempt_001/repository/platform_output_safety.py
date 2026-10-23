import boto3
from model_client import aws_region


def platform_output_safety(text):
    client = boto3.client("comprehend", region_name=aws_region())
    return client.detect_sensitive_data(Text=text, LanguageCode="en")
