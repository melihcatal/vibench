import boto3


def visual_safety_text(text):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"]
