import boto3


def get_s3_client():
    """
    Returns a configured boto3 S3 client.
    """
    return boto3.client("s3")


def get_textract_client():
    """
    Returns a configured boto3 Textract client.
    """
    return boto3.client("textract")


def get_translate_client():
    """
    Returns a configured boto3 Translate client.
    """
    return boto3.client("translate")


def get_bedrock_runtime_client():
    """
    Returns a configured boto3 Bedrock Runtime client.
    """
    return boto3.client("bedrock-runtime")
