import os


def get_document_client(region):
    return boto3.client("textract", region_name=region)