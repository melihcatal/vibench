import boto3


def payload_safety(plaintext):
    comprehend_client = boto3.client("comprehend")
    response = comprehend_client.detect_toxic_content(
        TextSegments=[{"Text": plaintext}]
    )
    return response["ResultList"][0]["Toxicity"]
