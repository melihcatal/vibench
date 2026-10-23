import boto3


def check_safety(text):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(TextSegments=[{"Text": text}])
    return response["ResultList"][0]["Toxicity"]["Label"] == "TOXIC"
