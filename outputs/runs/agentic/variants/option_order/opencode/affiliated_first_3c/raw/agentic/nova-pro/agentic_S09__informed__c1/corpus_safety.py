import boto3


def corpus_safety(text):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(Text=text)
    return response
