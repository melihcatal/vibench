import boto3


def record_text_safety(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(Text=text)
    return response["ToxicContent"]
