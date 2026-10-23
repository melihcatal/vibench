from boto3 import client


def payload_safety(text):
    comprehend_client = client("comprehend")
    response = comprehend_client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"]
