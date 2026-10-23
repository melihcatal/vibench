import boto3


def get_textract_client(region_name):
    return boto3.client("textract", region_name=region_name)

def get_translate_client(region_name):
    return boto3.client("translate", region_name=region_name)

def get_comprehend_client(region_name):
    return boto3.client("comprehend", region_name=region_name)

def get_bedrock_runtime_client(region_name):
    return boto3.client("bedrock-runtime", region_name=region_name)
