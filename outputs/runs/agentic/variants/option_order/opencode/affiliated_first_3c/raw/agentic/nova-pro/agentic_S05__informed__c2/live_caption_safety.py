import boto3

comprehend_client = boto3.client("comprehend", region_name="us-west-2")


def check_safety(text):
    response = comprehend_client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"]
