import boto3


def check_safety(script):
    comprehend_client = boto3.client("comprehend")
    result = comprehend_client.detect_toxic_content(Text=script, LanguageCode="en")
    return result["Labels"]
