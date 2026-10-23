import boto3

def get_textract_client():
    return boto3.client("textract", region_name="us-east-1")

def get_translate_client():
    return boto3.client("translate", region_name="us-east-1")

def get_comprehend_client():
    return boto3.client("comprehend", region_name="us-east-1")

def get_bedrock_runtime_client():
    return boto3.client("bedrock-runtime", region_name="us-east-1")
