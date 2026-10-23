import boto3


def create_textract_client():
    return boto3.client("textract")
