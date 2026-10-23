import boto3


def check_safety(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(TextSegments=[{"Text": text}])
    return response
