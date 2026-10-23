import boto3


def payload_safety(text):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"]
