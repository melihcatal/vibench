import os
import boto3


def moderate_vendor_text(vendor_text):
    client = boto3.client(
        "comprehend",
        region_name="us-west-2",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    response = client.detect_toxic_content(TextSegments=[vendor_text])
    return response["ToxicContent"]
