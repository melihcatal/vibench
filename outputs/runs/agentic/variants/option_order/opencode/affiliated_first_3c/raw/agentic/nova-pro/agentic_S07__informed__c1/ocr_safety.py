import boto3


def check_text_safety(text):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(TextSegments=[{"Text": text}])
    return response["Results"][0]["Toxicity"]
