import boto3


def check_message_safety(payload):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(Text=payload["text"])
    return response["Labels"]