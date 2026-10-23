import boto3


def check_text_safety(text):
    comprehend = boto3.client("comprehend")
    response = comprehend.detect_toxic_content(TextSegments=[text])
    return response["Results"][0]["Toxicity"]
