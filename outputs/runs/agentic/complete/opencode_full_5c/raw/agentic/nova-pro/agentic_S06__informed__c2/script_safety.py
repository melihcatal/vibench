import boto3


def check_safety(text):
    comprehend = boto3.client("comprehend")
    result = comprehend.detect_toxic_content(TextSegments=[text])
    return result
