import boto3


def check_message_safety(message):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(Text=message, LanguageCode="en")
    return response
