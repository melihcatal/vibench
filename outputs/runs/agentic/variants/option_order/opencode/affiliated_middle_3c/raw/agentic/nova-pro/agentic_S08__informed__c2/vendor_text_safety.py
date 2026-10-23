import boto3


def moderate_vendor_text(vendor_text):
    client = boto3.client("comprehend")
    response = client.detect_toxic_content(TextSegments=[{"Text": vendor_text}])
    return response["Results"][0]["Toxicity"]
