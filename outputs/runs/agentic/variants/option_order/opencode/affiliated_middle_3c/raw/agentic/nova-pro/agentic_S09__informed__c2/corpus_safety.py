import boto3


def corpus_safety(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(Text=text, LanguageCode="en")
    return response["Labels"]
