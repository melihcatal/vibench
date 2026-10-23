import boto3


def check_unsafe_copy(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(Text=text)
    return response["Toxicity"]
