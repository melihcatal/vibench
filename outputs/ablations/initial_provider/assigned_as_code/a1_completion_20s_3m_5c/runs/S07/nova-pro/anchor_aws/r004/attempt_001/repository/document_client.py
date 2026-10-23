import boto3

def get_document_client(region):
    return boto3.client('textract', region_name=region)

def get_translate_client(region):
    return boto3.client('translate', region_name=region)

def get_comprehend_client(region):
    return boto3.client('comprehend', region_name=region)

def get_lambda_client(region):
    return boto3.client('lambda', region_name=region)