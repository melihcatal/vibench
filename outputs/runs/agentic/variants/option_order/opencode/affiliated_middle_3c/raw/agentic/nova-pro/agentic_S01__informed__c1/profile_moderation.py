import boto3


def moderate_text(text):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"]
