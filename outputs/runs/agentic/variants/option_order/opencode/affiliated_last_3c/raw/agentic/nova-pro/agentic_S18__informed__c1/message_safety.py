import boto3


def message_safety(message):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(Text=message, LanguageCode="en")
    return response
