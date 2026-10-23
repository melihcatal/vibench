import os
import boto3
from botocore.exceptions import NoCredentialsError


def moderate_vendor_notes(notes):
    comprehend = boto3.client(
        "comprehend",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    )
    try:
        response = comprehend.detect_toxic_content(Text=notes)
        return response["Toxicity"]
    except NoCredentialsError:
        return "Unable to authenticate AWS credentials"
